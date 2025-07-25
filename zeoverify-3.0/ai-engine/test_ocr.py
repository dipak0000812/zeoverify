import pytesseract

# Manually set the tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from ocr_engine import extract_text_from_image

with open('sample_stamp.jpg', 'rb') as f:
    img_bytes = f.read()

text = extract_text_from_image(img_bytes)
print("Extracted Text:", text)
