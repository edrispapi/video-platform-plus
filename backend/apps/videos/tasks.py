import cv2
from celery import shared_task
from apps.videos.models import Video # استفاده از مسیر اپلیکیشن‌ها
from ai_engine.logo_utils import detect_logo_box, inpaint_logo

@shared_task(bind=True)
def process_video_for_branding_removal(self, video_id):
    """
    وظیفه Celery برای پردازش ویدئو: حذف لوگوهای ثابت و واترمارک صوتی.
    """
    try:
        video_obj = Video.objects.get(id=video_id)
        input_video_path = video_obj.file.path
        output_video_path = input_video_path.replace('.mp4', '_branded_clean.mp4')

        # مرحله 1: حذف لوگوهای تصویری
        # (این بخش فرض می‌کند که ai_engine/logo_utils.py واقعاً این کار را انجام می‌دهد)
        temp_no_logo_video_path = input_video_path.replace('.mp4', '_temp_no_logo.mp4')
        process_video_logo_removal(input_video_path, temp_no_logo_video_path)

        # مرحله 2: حذف واترمارک صوتی (جینگل‌ها)
        # (این بخش فرض می‌کند که ai_engine/audio_utils.py واقعاً این کار را انجام می‌دهد)
        from ai_engine.audio_utils import remove_audio_watermark
        temp_no_audio_watermark_video_path = output_video_path # نام فایل نهایی
        remove_audio_watermark(temp_no_logo_video_path, temp_no_audio_watermark_video_path)

        # به‌روزرسانی مدل ویدئو در دیتابیس
        video_obj.processed_file.name = temp_no_audio_watermark_video_path # مسیر فایل نهایی
        video_obj.status = 'processed_cleaned'
        video_obj.save()

        # حذف فایل موقت
        # os.remove(temp_no_logo_video_path)

    except Video.DoesNotExist:
        print(f"Video with ID {video_id} not found.")
        self.retry(exc=Video.DoesNotExist, countdown=60, max_retries=3)
    except Exception as e:
        print(f"Error processing video {video_id}: {e}")
        self.retry(exc=e, countdown=300, max_retries=5)

# تابع کمکی برای حذف لوگو (فراخوانی از tasks.py)
def process_video_logo_removal(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # یا 'H264'
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # تشخیص لوگو
        logo_bbox = detect_logo_box(frame) # از ai_engine.logo_utils
        if logo_bbox:
            # حذف لوگو
            frame = inpaint_logo(frame, logo_bbox) # از ai_engine.logo_utils
        out.write(frame)

    cap.release()
    out.release()
