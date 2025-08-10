#!/usr/bin/env python3
"""
Test script to verify all improvements to the Zeoverify API.
Run this after starting the Flask server to test all endpoints.
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health_endpoint():
    """Test the health check endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_text_verification():
    """Test text-based verification endpoint."""
    print("\n🔍 Testing text verification endpoint...")
    try:
        test_text = "This is a sample real estate document for testing purposes."
        data = {"certificate_text": test_text}
        response = requests.post(f"{BASE_URL}/verify", json=data)
        print(f"✅ Text verification: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Text verification failed: {e}")
        return False

def test_file_upload_verification():
    """Test file upload verification endpoint."""
    print("\n🔍 Testing file upload verification...")
    try:
        # Create a simple test file
        test_content = "This is a test PDF document content for verification."
        files = {'file': ('test_document.txt', test_content, 'text/plain')}
        
        response = requests.post(f"{BASE_URL}/api/verify", files=files)
        print(f"✅ File upload verification: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ File upload verification failed: {e}")
        return False

def test_error_handling():
    """Test error handling for invalid requests."""
    print("\n🔍 Testing error handling...")
    
    # Test 1: No file uploaded
    try:
        response = requests.post(f"{BASE_URL}/api/verify")
        print(f"✅ No file error: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ No file error test failed: {e}")
    
    # Test 2: Empty JSON data
    try:
        response = requests.post(f"{BASE_URL}/verify", json={})
        print(f"✅ Empty JSON error: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Empty JSON error test failed: {e}")
    
    # Test 3: Invalid endpoint
    try:
        response = requests.get(f"{BASE_URL}/invalid_endpoint")
        print(f"✅ 404 error: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ 404 error test failed: {e}")

def test_model_integration():
    """Test that the ML model is working correctly."""
    print("\n🔍 Testing ML model integration...")
    try:
        # Test with different types of text
        test_cases = [
            "real estate property agreement sale deed",
            "fake document certificate verification",
            "random text content for testing"
        ]
        
        for i, test_text in enumerate(test_cases, 1):
            data = {"certificate_text": test_text}
            response = requests.post(f"{BASE_URL}/verify", json=data)
            print(f"   Test {i}: {test_text[:30]}... -> {response.json()}")
            time.sleep(0.5)  # Small delay between requests
        
        return True
    except Exception as e:
        print(f"❌ ML model integration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Zeoverify API Tests...\n")
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Text Verification", test_text_verification),
        ("File Upload Verification", test_file_upload_verification),
        ("Error Handling", test_error_handling),
        ("ML Model Integration", test_model_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    print('='*50)
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")

if __name__ == "__main__":
    main()
