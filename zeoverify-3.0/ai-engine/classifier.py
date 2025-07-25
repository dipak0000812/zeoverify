# classifier.py

def classify_document(text):
    """
    Classifies document type based on keywords in extracted text.
    """
    text = text.lower()
    
    if "rental agreement" in text or "lease deed" in text:
        return "Rental Agreement"
    elif "income tax department" in text or "permanent account number" in text:
        return "PAN Card"
    elif "government of india" in text and "aadhaar" in text:
        return "Aadhaar Card"
    elif "birth certificate" in text:
        return "Birth Certificate"
    elif "driving licence" in text or "driver license" in text:
        return "Driving License"
    else:
        return "Unknown Document"


# test code
if __name__ == "__main__":
    sample_text = """
    This is a RENTAL AGREEMENT between Mr. X and Mr. Y
    """
    doc_type = classify_document(sample_text)
    print(f"Predicted Document Type: {doc_type}")
