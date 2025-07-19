"""Celery tasks for AI video processing and FFmpeg operations"""
import subprocess
from celery import shared_task
from videos.models import Video

@shared_task(bind=True)
def process_video_ai(self, video_id):
    """Process video: remove background noise, remove logo, repackage video"""
    try:
        video_obj = Video.objects.get(id=video_id)
        input_file = video_obj.file.path
        output_file = input_file.replace('.mp4', '_processed.mp4')

        # مرحله ۱: استخراج صدا
        audio_file = input_file.replace('.mp4', '.wav')
        cmd_audio_extract = ['ffmpeg', '-y', '-i', input_file, '-vn', audio_file]
        subprocess.run(cmd_audio_extract, check=True)

        # مرحله ۲: فراخوانی مدل AI برای حذف صدای پس‌زمینه
        from .ai_utils import remove_background_noise
        clean_audio = remove_background_noise(audio_file)

        # مرحله ۳: حذف لوگو با AI
        from .ai_utils import remove_logo_from_video
        processed_video_path = remove_logo_from_video(input_file)

        # مرحله ۴: ترکیب دوباره تصویر و صدای پردازش شده
        cmd_combine = [
            'ffmpeg', '-y',
            '-i', processed_video_path,
            '-i', clean_audio,
            '-c:v', 'copy',
            '-c:a', 'aac',
            output_file
        ]
        subprocess.run(cmd_combine, check=True)

        # مرحله ۵: بروزرسانی وضعیت
        video_obj.processed_file.name = output_file
        video_obj.status = 'processed'
        video_obj.save()

        return True
    except Exception as e:
        self.retry(exc=e, countdown=60, max_retries=3)
