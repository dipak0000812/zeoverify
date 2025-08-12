# ai-engine/fraud_checker.py
import re
from typing import Tuple, List

class FraudDetector:
    """Advanced fraud detection for real estate documents."""
    
    def __init__(self):
        """Initialize the fraud detector."""
        self.suspicious_keywords = [
            'fake', 'forgery', 'invalid', 'suspicious', 'fraudulent', 
            'not paid', 'missing', 'no valid', 'warning', 'red flags',
            'void', 'cancelled', 'expired', 'unauthorized', 'illegal'
        ]
        
        self.essential_elements = {
            'rera_certificate': [
                'certificate no', 'registration', 'maharashtra rera', 'karnataka rera',
                'real estate regulatory authority', 'project registration'
            ],
            'sale_deed': [
                'stamp duty', 'registration', 'sub-registrar', 'plot no', 'survey no',
                'property address', 'consideration amount', 'seller', 'buyer'
            ],
            'lease_agreement': [
                'lessor', 'lessee', 'landlord', 'tenant', 'rent', 'lease period',
                'property address', 'security deposit', 'terms and conditions'
            ]
        }
    
    def analyze_document(self, text: str) -> Tuple[float, List[str]]:
        """
        Analyze document for fraud indicators and return risk score with issues.
        
        Args:
            text: Extracted text from document
            
        Returns:
            Tuple of (risk_score, list_of_issues)
        """
        if not text.strip():
            return 100.0, ["Empty document"]
        
        issues = []
        risk_score = 0
        
        # Convert text to lowercase for analysis
        text_lower = text.lower()
        
        # Check for suspicious keywords
        for keyword in self.suspicious_keywords:
            if keyword in text_lower:
                issues.append(f"Contains suspicious keyword: '{keyword}'")
                risk_score += 15
        
        # Check for missing essential elements based on document type
        document_type = self._detect_document_type(text_lower)
        if document_type in self.essential_elements:
            missing_elements = self._check_missing_elements(text_lower, document_type)
            for element in missing_elements:
                issues.append(f"Missing essential element: {element}")
                risk_score += 10
        
        # Check for completely unrelated documents
        if self._is_unrelated_document(text_lower):
            issues.append("Document appears unrelated to real estate")
            risk_score += 50
        
        # Check for proper formatting and structure
        if len(text.strip()) < 50:
            issues.append("Document content too short")
            risk_score += 20
        
        # Check for suspicious patterns
        suspicious_patterns = self._check_suspicious_patterns(text_lower)
        issues.extend(suspicious_patterns)
        risk_score += len(suspicious_patterns) * 10
        
        # Normalize risk score to 0-100
        risk_score = min(100, risk_score)
        
        return risk_score, issues
    
    def _detect_document_type(self, text_lower: str) -> str:
        """Detect document type for targeted fraud analysis."""
        if any(keyword in text_lower for keyword in ['rera', 'certificate', 'registration']):
            return 'rera_certificate'
        elif any(keyword in text_lower for keyword in ['sale deed', 'deed of sale', 'conveyance']):
            return 'sale_deed'
        elif any(keyword in text_lower for keyword in ['lease', 'rental', 'agreement']):
            return 'lease_agreement'
        else:
            return 'unknown'
    
    def _check_missing_elements(self, text_lower: str, document_type: str) -> List[str]:
        """Check for missing essential elements in the document."""
        missing = []
        required_elements = self.essential_elements.get(document_type, [])
        
        for element in required_elements:
            if element not in text_lower:
                missing.append(element)
        
        return missing
    
    def _is_unrelated_document(self, text_lower: str) -> bool:
        """Check if document is unrelated to real estate."""
        unrelated_keywords = [
            'resume', 'cv', 'curriculum vitae', 'job', 'employment', 
            'tax invoice', 'bill', 'ticket', 'receipt', 'medical', 'prescription'
        ]
        return any(keyword in text_lower for keyword in unrelated_keywords)
    
    def _check_suspicious_patterns(self, text_lower: str) -> List[str]:
        """Check for suspicious patterns in the document."""
        patterns = []
        
        # Check for inconsistent dates
        if self._has_inconsistent_dates(text_lower):
            patterns.append("Inconsistent or suspicious dates")
        
        # Check for missing signatures
        if 'signature' not in text_lower and 'signed' not in text_lower:
            patterns.append("No signature information found")
        
        # Check for suspicious amounts
        if self._has_suspicious_amounts(text_lower):
            patterns.append("Suspicious or unrealistic amounts")
        
        return patterns
    
    def _has_inconsistent_dates(self, text_lower: str) -> bool:
        """Check for inconsistent or suspicious dates."""
        # This is a simplified check - you can make it more sophisticated
        date_patterns = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text_lower)
        if len(date_patterns) > 1:
            # Check if dates are reasonable (not too far apart, not in future, etc.)
            return False  # Simplified for now
        return False
    
    def _has_suspicious_amounts(self, text_lower: str) -> bool:
        """Check for suspicious or unrealistic amounts."""
        # Look for amounts that might be suspicious
        amount_patterns = re.findall(r'rs\.?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text_lower)
        for amount in amount_patterns:
            # Extract numeric value
            numeric_value = re.sub(r'[^\d.]', '', amount)
            try:
                value = float(numeric_value)
                # Check for suspicious amounts (too low or too high)
                if value < 1000 or value > 1000000000:  # Less than 1K or more than 1B
                    return True
            except ValueError:
                continue
        return False

def check_fraud(text):
    """Legacy function for backward compatibility."""
    detector = FraudDetector()
    risk_score, issues = detector.analyze_document(text)
    return risk_score, issues
