import tensorflow as tf
from celery import shared_task
from .safe_content import analyze_content
from django.core.files.storage import default_storage
import numpy as np
import os

@shared_task
def process_video_for_branding_removal(video_id):
    # کد قبلی برای حذف برند حفظ می‌شه
    pass

@shared_task
def moderate_content(video_id, content_type='video'):
    if content_type == 'video':
        video_path = default_storage.path(f'videos/video_{video_id}.mp4')
        model = tf.keras.models.load_model('path/to/moderation_model.h5')  # مدل پیش‌آموزش‌دیده
        # تبدیل ویدئو به فریم‌ها (ساده‌سازی)
        frames = extract_frames(video_path)
        predictions = model.predict(np.array(frames))
        if np.any(predictions > 0.5):  # آستانه برای محتوای نامناسب
            return {'status': 'rejected', 'reason': 'Inappropriate content detected'}
        return {'status': 'approved'}
    elif content_type == 'comment':
        text = content_type  # فرض می‌کنیم text به‌عنوان ورودی ارسال شده
        result = analyze_content(text)  # فرض می‌کنیم تابع موجوده
        return {'status': 'approved' if result['safe'] else 'rejected', 'reason': result.get('reason')}

def extract_frames(video_path, max_frames=10):
    # تابع ساده برای استخراج فریم‌ها (نیاز به opencv)
    import cv2
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    while cap.isOpened() and count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(cv2.resize(frame, (224, 224)))  # اندازه مناسب مدل
        count += 1
    cap.release()
    return frames
