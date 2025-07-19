from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

def ocr_transformers(image_path):
    """استخراج متن از تصویر با TrOCR"""
    processor = TrOCRProcessor.from_pretrained("microsoft/trocr-small-stage1")
    model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-small-stage1")
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
