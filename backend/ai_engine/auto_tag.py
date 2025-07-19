def auto_tag_video(frame, vision_model):
    """تگ‌زنی خودکار بر اساس تحلیل فریم"""
    detected_classes = vision_model.predict(frame)  # فرض: خروجی مدل ['dog', 'logo', 'nature']
    return detected_classes
