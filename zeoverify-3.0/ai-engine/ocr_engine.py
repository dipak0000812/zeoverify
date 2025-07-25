# ocr_engine.py
import pytesseract
from PIL import Image
import io

def extract_text_from_image(image_bytes):
    """
    Extract text from image bytes using pytesseract OCR.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image, lang='eng')
        return text.strip()
    except Exception as e:
        print(f"[OCR ERROR]: {e}")
        return ""
