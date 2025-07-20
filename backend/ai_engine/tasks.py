import tensorflow as tf
from celery import shared_task
from .safe_content import analyze_content
from django.core.files.storage import default_storage
import numpy as np
import os
from kafka import KafkaConsumer
import json

@shared_task
def process_video_for_branding_removal(video_id):
    # کد قبلی برای حذف برند
    pass

@shared_task
def moderate_content(video_id, content_type='video'):
    if content_type == 'video':
        video_path = default_storage.path(f'videos/video_{video_id}.mp4')
        model = tf.keras.models.load_model('path/to/moderation_model.h5')
        frames = extract_frames(video_path)
        predictions = model.predict(np.array(frames))
        if np.any(predictions > 0.5):
            return {'status': 'rejected', 'reason': 'Inappropriate content detected'}
        return {'status': 'approved'}
    elif content_type == 'comment':
        text = content_type  # فرض می‌کنیم text به‌عنوان ورودی ارسال شده
        result = analyze_content(text)
        return {'status': 'approved' if result['safe'] else 'rejected', 'reason': result.get('reason')}

def extract_frames(video_path, max_frames=10):
    import cv2
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    while cap.isOpened() and count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(cv2.resize(frame, (224, 224)))
        count += 1
    cap.release()
    return frames

@shared_task
def process_stream_analytics():
    consumer = KafkaConsumer(
        'video_events',
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    for message in consumer:
        event = message.value
        # ذخیره در Data Lake (مثلاً MinIO)
        save_to_datalake(event)
        # تحلیل ساده (مثلاً تعداد لایک‌ها)
        if event['event_type'] == 'like':
            print(f"Like event for video {event['video_id']} by user {event['user_id']}")

def save_to_datalake(event):
    from minio import Minio
    client = Minio(
        'minio:9000',
        access_key='your_access_key',
        secret_key='your_secret_key',
        secure=False
    )
    client.put_object(
        'video-analytics',
        f"events/{event['timestamp'].replace(':', '-')}.json",
        io.BytesIO(json.dumps(event).encode('utf-8')),
        length=-1,
        part_size=10*1024*1024
    )
