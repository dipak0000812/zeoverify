#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints are working.
Run this while the Flask API is running.
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test the health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_text_verification():
    """Test the text verification endpoint."""
    try:
        test_text = "This is a real estate document with property details and ownership information."
        data = {"certificate_text": test_text}
        response = requests.post(f"{BASE_URL}/verify", json=data)
        print(f"✅ Text verification: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Text verification failed: {e}")
        return False

def test_file_verification():
    """Test the file verification endpoint."""
    try:
        # Create a simple test file
        test_content = "This is a test document for verification purposes."
        with open("test_document.txt", "w") as f:
            f.write(test_content)
        
        # Test file upload
        with open("test_document.txt", "rb") as f:
            files = {"file": ("test_document.txt", f, "text/plain")}
            response = requests.post(f"{BASE_URL}/api/verify", files=files)
        
        print(f"✅ File verification: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Clean up test file
        import os
        os.remove("test_document.txt")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ File verification failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing API endpoints...")
    print("=" * 50)
    
    # Test all endpoints
    health_ok = test_health()
    text_ok = test_text_verification()
    file_ok = test_file_verification()
    
    print("=" * 50)
    print("📊 Test Results:")
    print(f"Health endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Text verification: {'✅ PASS' if text_ok else '❌ FAIL'}")
    print(f"File verification: {'✅ PASS' if file_ok else '❌ FAIL'}")
    
    if all([health_ok, text_ok, file_ok]):
        print("\n🎉 All tests passed! Your API is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the API logs for details.")
