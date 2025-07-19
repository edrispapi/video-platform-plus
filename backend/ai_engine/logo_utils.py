import cv2
import numpy as np

def detect_logo_box(frame, confidence_threshold=0.5):
    """
    شناسایی خودکار محل لوگو در فریم با مدل YOLO/Detectron2 (نصب جداگانه).
    خروجی: مختصات [x1, y1, x2, y2] یا None
    در صورت نبود مدل، روی گوشه بالا-راست fallback می‌شود.
    """
    try:
        # اتصال به مدل، نمونه انطباق با پروژه خود قرار دهید:
        # net = cv2.dnn.readNet(YOLO_MODEL_WEIGHTS, YOLO_MODEL_CFG)
        # ... پردازش فریم با مدل ...
        # خروجی واقعی از مدل قرار دهید: [(x1, y1, x2, y2), ...]
        pass  # جایگزین با مدل اختصاصی شما
    except Exception:
        pass  # برای مواقعی که مدل نیست

    h, w = frame.shape[:2]
    x1, y1, x2, y2 = w-120, 10, w-10, 60
    return (x1, y1, x2, y2)

def inpaint_logo(frame, bbox):
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.rectangle(mask, (bbox[0], bbox[1]), (bbox[2], bbox[3]), 255, -1)
    return cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)
