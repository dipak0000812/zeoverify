
# ai-engine/ocr.pyimport cv2
import cv2
import numpy as np
import easyocr
 
from PIL import Image

reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image_path):
    # Read image
    img = cv2.imread(image_path)
    # Convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Thresholding (remove background)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Optional: denoise
    denoised = cv2.fastNlMeansDenoising(thresh, h=30)

    # OCR
    result = reader.readtext(denoised, detail=0)
    return " ".join(result)
