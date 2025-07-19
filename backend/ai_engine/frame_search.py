import cv2
import pytesseract

def frame_texts(video_path, interval=30):
    """
    استخراج متن از فریم‌های ویدیو (هر ۳۰ فریم یکبار) با OCR
    """
    cap = cv2.VideoCapture(video_path)
    frame_no = 0
    frame_texts = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_no % interval == 0:
            text = pytesseract.image_to_string(frame, lang='fas')
            frame_texts.append((frame_no, text))
        frame_no += 1
    cap.release()
    return frame_texts
