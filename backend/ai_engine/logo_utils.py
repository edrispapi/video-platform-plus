import cv2
import numpy as np
from ai_engine.vision_ai import detect_logo_yolov8  # فرض می‌کنیم vision_ai.py نصب شده

def detect_logo_box(frame, confidence_threshold=0.5):
    """
    شناسایی خودکار محل لوگو در فریم با مدل YOLOv8 (نصب جداگانه).
    خروجی: مختصات [x1, y1, x2, y2] یا None
    در صورت نبود مدل، روی گوشه بالا-راست fallback می‌شود.
    """
    try:
        boxes = detect_logo_yolov8(frame, 'yolov8.pt')
        return boxes[0] if boxes else None
    except Exception:
        h, w = frame.shape[:2]
        x1, y1, x2, y2 = w-120, 10, w-10, 60
        return (x1, y1, x2, y2)

def inpaint_logo(frame, bbox):
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.rectangle(mask, (bbox[0], bbox[1]), (bbox[2], bbox[3]), 255, -1)
    return cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)
