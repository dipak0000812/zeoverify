#!/usr/bin/env python3
"""
Test script to verify document classification improvements
"""

from fraud_checker import check_fraud
from ml_model.predict import predict_doc_type_ml

def test_document_classification():
    # Test cases with different document types
    test_cases = [
        {
            "name": "Real RERA Certificate",
            "text": "Maharashtra RERA Registration Certificate issued under section 9. Certificate No: MAHREA/RERA/2023/001234. This certificate is issued by Maharashtra Real Estate Regulatory Authority (MahaRERA) and is valid for all legal purposes.",
            "expected_type": "real",
            "expected_risk": "low"
        },
        {
            "name": "Fake RERA Certificate",
            "text": "This is a fake RERA certificate without valid number. The project claims to be registered but this certificate is not issued by any legitimate authority. WARNING: This certificate is fake and should not be used for any legal purposes.",
            "expected_type": "fake",
            "expected_risk": "high"
        },
        {
            "name": "Real Sale Deed",
            "text": "DEED OF SALE executed between seller and purchaser in Mumbai. Stamp Duty Paid: Rs. 50,000. Registered at: Sub-Registrar Office, Andheri, Mumbai. Registration No: 2023/12345.",
            "expected_type": "real",
            "expected_risk": "low"
        },
        {
            "name": "Fake Sale Deed",
            "text": "This is a forgery sale deed missing stamp duty. This document appears to be a sale deed but contains several red flags. Stamp Duty: NOT PAID. Registration Fee: NOT PAID. This document is clearly a forgery.",
            "expected_type": "fake",
            "expected_risk": "high"
        },
        {
            "name": "Resume (Invalid)",
            "text": "CURRICULUM VITAE - John Doe. Bachelor of Technology in Computer Science. Software Developer with experience in Python and React. This is a completely unrelated document to real estate verification.",
            "expected_type": "invalid",
            "expected_risk": "high"
        }
    ]
    
    print("🧪 Testing Document Classification System")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📄 Test {i}: {test_case['name']}")
        print("-" * 30)
        
        # Test ML classification
        doc_type = predict_doc_type_ml(test_case['text'])
        
        # Test fraud detection
        fraud_risk, fraud_issues = check_fraud(test_case['text'])
        
        print(f"📝 Document Type: {doc_type}")
        print(f"⚠️  Fraud Risk: {fraud_risk}%")
        print(f"🔍 Issues Found: {len(fraud_issues)}")
        
        if fraud_issues:
            for issue in fraud_issues:
                print(f"   • {issue}")
        
        # Check if results match expectations
        type_correct = doc_type == test_case['expected_type']
        risk_level = "low" if fraud_risk < 30 else "medium" if fraud_risk < 70 else "high"
        risk_correct = risk_level == test_case['expected_risk']
        
        print(f"✅ Type Correct: {type_correct}")
        print(f"✅ Risk Level Correct: {risk_correct}")
        
        if not type_correct or not risk_correct:
            print(f"❌ Expected: {test_case['expected_type']} document with {test_case['expected_risk']} risk")
        else:
            print("🎉 All tests passed for this document!")

if __name__ == "__main__":
    test_document_classification() 