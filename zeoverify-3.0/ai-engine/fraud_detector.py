# fraud_detector.py
import re

def detect_fraud(text):
    """
    Detects possible fraud based on suspicious patterns in text.
    Returns True if suspicious, else False.
    """
    text = text.lower()

    suspicious_patterns = [
        r"fake",
        r"duplicate",
        r"forged",
        r"not valid",
        r"sample",
        r"specimen"
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, text):
            return True

    return False

# Optional: test run
if __name__ == "__main__":
    sample_text = "This document is a FAKE rental agreement used for testing."
    is_fraud = detect_fraud(sample_text)
    print(f"Fraud Detected? {is_fraud}")
