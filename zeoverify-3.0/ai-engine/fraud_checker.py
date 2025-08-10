# ai-engine/fraud_checker.py
import re

def check_fraud(text):
    issues = []
    risk_score = 0
    
    # Convert text to lowercase for analysis
    text_lower = text.lower()
    
    # Check for suspicious keywords and patterns
    suspicious_keywords = [
        'fake', 'forgery', 'invalid', 'suspicious', 'fraudulent', 
        'not paid', 'missing', 'no valid', 'warning', 'red flags'
    ]
    
    for keyword in suspicious_keywords:
        if keyword in text_lower:
            issues.append(f"Contains suspicious keyword: '{keyword}'")
            risk_score += 15
    
    # Check for missing essential elements in real estate documents
    if any(doc_type in text_lower for doc_type in ['rera', 'certificate', 'registration']):
        # RERA certificate checks
        if 'maharashtra rera' in text_lower or 'karnataka rera' in text_lower:
            if 'certificate no' not in text_lower:
                issues.append("Missing certificate number")
                risk_score += 10
            if 'registration' not in text_lower:
                issues.append("Missing registration details")
                risk_score += 10
        else:
            issues.append("Suspicious RERA certificate format")
            risk_score += 20
    
    elif any(doc_type in text_lower for doc_type in ['sale deed', 'deed of sale']):
        # Sale deed checks
        if 'stamp duty' not in text_lower or 'not paid' in text_lower:
            issues.append("Missing or unpaid stamp duty")
            risk_score += 25
        if 'registration' not in text_lower:
            issues.append("Missing registration details")
            risk_score += 15
        if 'sub-registrar' not in text_lower:
            issues.append("Missing sub-registrar mention")
            risk_score += 10
    
    elif any(doc_type in text_lower for doc_type in ['lease', 'rental', 'agreement']):
        # Lease agreement checks
        if 'lessor' not in text_lower and 'landlord' not in text_lower:
            issues.append("Missing lessor/landlord details")
            risk_score += 10
        if 'lessee' not in text_lower and 'tenant' not in text_lower:
            issues.append("Missing lessee/tenant details")
            risk_score += 10
        if 'rent' not in text_lower and 'lease period' not in text_lower:
            issues.append("Missing rent/lease terms")
            risk_score += 15
    
    # Check for completely unrelated documents
    unrelated_keywords = ['resume', 'cv', 'curriculum vitae', 'job', 'employment', 'tax invoice', 'bill', 'ticket']
    if any(keyword in text_lower for keyword in unrelated_keywords):
        issues.append("Document appears unrelated to real estate")
        risk_score += 50
    
    # Check for proper formatting and structure
    if len(text.strip()) < 50:
        issues.append("Document content too short")
        risk_score += 20
    
    # Normalize risk score to 0-100
    risk_score = min(100, risk_score)
    
    return risk_score, issues
