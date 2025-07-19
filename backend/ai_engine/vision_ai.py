import cv2
import numpy as np
import torch
from ultralytics import YOLO
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg

def detect_logo_yolov8(frame, model_path='yolov8.pt'):
    """تشخیص لوگو با YOLOv8"""
    model = YOLO(model_path)
    results = model.predict(frame)
    boxes = [(int(x1), int(y1), int(x2), int(y2)) for x1, y1, x2, y2, score, cls in results[0].boxes.data.tolist() if score > 0.5 and cls == 0]
    return boxes

def detect_objects_detectron2(frame, model_config, model_weights):
    """تشخیص اشیا با Detectron2"""
    cfg = get_cfg()
    cfg.merge_from_file(model_config)
    cfg.MODEL.WEIGHTS = model_weights
    predictor = DefaultPredictor(cfg)
    outputs = predictor(frame)
    return outputs["instances"].pred_boxes.tensor.cpu().numpy()
