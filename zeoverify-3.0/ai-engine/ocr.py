
# ai-engine/ocr.py
import cv2
import numpy as np
import easyocr
import fitz  # PyMuPDF for PDF processing
from PIL import Image
import os

reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image_path):
    """Extract text from image files using EasyOCR."""
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
            
        # Convert to gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Thresholding (remove background)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Optional: denoise
        denoised = cv2.fastNlMeansDenoising(thresh, h=30)

        # OCR
        result = reader.readtext(denoised, detail=0)
        return " ".join(result)
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF files using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_file(file_path):
    """Extract text from various file types (PDF, images, text files)."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return extract_text_from_pdf(file_path)
        elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']:
            return extract_text(file_path)
        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # Try OCR for unknown file types
            return extract_text(file_path)
            
    except Exception as e:
        print(f"Error extracting text from file {file_path}: {e}")
        return ""
