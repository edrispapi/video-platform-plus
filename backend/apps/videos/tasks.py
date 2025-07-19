import cv2
from celery import shared_task
from apps.videos.models import Video
from .logo_utils import detect_logo_box, inpaint_logo
from .audio_utils import remove_audio_watermark

def process_video_logo_removal(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    while True:
        ret, frame = cap.read()
        if not ret: break
        bbox = detect_logo_box(frame)
        if bbox: frame = inpaint_logo(frame, bbox)
        out.write(frame)
    cap.release()
    out.release()

@shared_task(bind=True)
def process_video_for_branding_removal(self, video_id):
    try:
        video_obj = Video.objects.get(id=video_id)
        input_video_path = video_obj.file.path
        temp_no_logo_video_path = input_video_path.replace('.mp4', '_temp_no_logo.mp4')
        output_video_path = input_video_path.replace('.mp4', '_branded_clean.mp4')
        process_video_logo_removal(input_video_path, temp_no_logo_video_path)
        from .audio_utils import remove_audio_watermark
        remove_audio_watermark(temp_no_logo_video_path, output_video_path)
        video_obj.processed_file.name = output_video_path
        video_obj.status = 'processed_cleaned'
        video_obj.save()
    except Video.DoesNotExist:
        print(f"Video with ID {video_id} not found.")
        self.retry(exc=Video.DoesNotExist, countdown=60, max_retries=3)
    except Exception as e:
        print(f"Error processing video {video_id}: {e}")
        self.retry(exc=e, countdown=300, max_retries=5)
