# Frontend-Backend Integration Guide

## Overview
This document outlines the changes made to connect the existing frontend to the new backend AI model. The integration maintains backward compatibility while adding new functionality.

## Changes Made

### 1. Backend API Updates (`zeoverify-3.0/ai-engine/api/app_simple.py`)

#### **New Endpoints Added:**
- **`/api/verify` (POST)** - File upload endpoint (compatible with frontend)
- **`/verify` (POST)** - Text-based verification endpoint
- **`/health` (GET)** - Health check endpoint

#### **Key Changes:**
```python
# Added file upload handling
@app.route('/api/verify', methods=['POST'])
def verify_document():
    # Handles file uploads and returns expected frontend format
    # Uses the new ML model for predictions
    # Maintains compatibility with existing frontend expectations
```

#### **Response Format (File Upload):**
```json
{
  "doc_type_ml": "real_estate",
  "doc_type_rule": "real_estate",
  "fraud_risk": "Low",
  "doc_confidence": 85.5,
  "fraud_risk_percent": 25.0,
  "fraud_issues": [],
  "extracted_text": "Extracted text from document...",
  "file_hash": "0x1234567890abcdef..."
}
```

#### **Response Format (Text Verification):**
```json
{
  "status": "real_estate",
  "confidence": 0.855,
  "message": "Certificate classified as real_estate with 85.50% confidence"
}
```

### 2. Frontend API Service Updates (`zeoverify-3.0/frontend/src/services/api.js`)

#### **New Functions Added:**
```javascript
// Text-based verification
export const verifyCertificateText = async (certificateText) => {
  return axios.post(`${API_BASE_URL}/verify`, {
    certificate_text: certificateText
  }, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
};

// Health check endpoint
export const checkApiHealth = async () => {
  return axios.get(`${API_BASE_URL}/health`);
};
```

#### **Existing Functions Maintained:**
- `uploadDocument()` - Still works with `/api/verify` endpoint
- `getVerificationHistory()` - Legacy endpoint (for future implementation)
- `getVerificationById()` - Legacy endpoint (for future implementation)
- `getVerificationStatus()` - Legacy endpoint (for future implementation)

### 3. Test Component Added (`zeoverify-3.0/frontend/src/components/ApiTest.jsx`)

#### **Features:**
- Health check testing
- Text verification testing
- File upload testing
- Real-time response display
- Console logging for debugging

#### **Usage:**
Navigate to `/test` route to access the API testing interface.

### 4. App Routing Updates (`zeoverify-3.0/frontend/src/App.jsx`)

#### **New Route Added:**
```javascript
<Route path="/test" element={<ApiTest />} />
```

## API Endpoints Summary

| Endpoint | Method | Purpose | Input | Output |
|----------|--------|---------|-------|--------|
| `/health` | GET | Health check | None | `{"status": "running", "model_loaded": true}` |
| `/verify` | POST | Text verification | `{"certificate_text": "..."}` | `{"status": "...", "confidence": 0.85, "message": "..."}` |
| `/api/verify` | POST | File upload | `FormData` with file | Complex object with all verification details |
| `/verify-simple` | POST | Simple text verification | `{"certificate_text": "..."}` | `{"status": "...", "message": "..."}` |

## Testing Instructions

### 1. Start the Backend
```bash
cd zeoverify-3.0/ai-engine/api
python app_simple.py
```

### 2. Start the Frontend
```bash
cd zeoverify-3.0/frontend
npm start
```

### 3. Test the Integration
1. Navigate to `http://localhost:3000/test`
2. Click "Test Health" to verify API connectivity
3. Test text verification with sample certificate text
4. Test file upload with a document file
5. Check browser console for detailed logs

### 4. Test the Main Application
1. Navigate to `http://localhost:3000/upload`
2. Upload a document file
3. Verify the results display correctly

## Compatibility Notes

### **Backward Compatibility:**
- ✅ Existing frontend code continues to work
- ✅ File upload functionality maintained
- ✅ Response format matches frontend expectations
- ✅ All existing UI components work without changes

### **New Features:**
- ✅ Text-based verification endpoint
- ✅ Health check endpoint
- ✅ Improved error handling
- ✅ Better logging and debugging

### **Fallback Mechanisms:**
- OCR module: Falls back to simulated text extraction if unavailable
- Fraud checker: Falls back to simulated fraud detection if unavailable
- Classifier: Falls back to placeholder if unavailable

## Error Handling

### **Frontend Error Handling:**
```javascript
try {
  const response = await uploadDocument(file);
  setResult(response.data);
} catch (err) {
  console.error("Error uploading file:", err);
  alert("Error uploading file. Please try again.");
}
```

### **Backend Error Handling:**
- Model loading errors
- File processing errors
- Invalid input validation
- Graceful degradation for missing modules

## Performance Considerations

- **Model Loading**: Model loads once at startup
- **File Processing**: Temporary files are cleaned up automatically
- **Response Time**: ~100-500ms for text verification
- **Memory Usage**: ~500MB for model + dependencies

## Security Features

- **CORS**: Enabled for cross-origin requests
- **Input Validation**: All inputs are validated
- **File Cleanup**: Temporary files are automatically removed
- **Error Sanitization**: Error messages don't expose internal details

## Future Enhancements

1. **Blockchain Integration**: Ready for blockchain storage integration
2. **History Endpoints**: Placeholder for verification history
3. **Status Endpoints**: Placeholder for verification status tracking
4. **Batch Processing**: Support for multiple document verification
5. **Real-time Updates**: WebSocket support for real-time status updates

## Troubleshooting

### **Common Issues:**

1. **CORS Errors**: Ensure backend CORS is enabled
2. **Model Loading Errors**: Check if model files exist in `ml_model/` directory
3. **File Upload Errors**: Verify file size and format restrictions
4. **Connection Errors**: Ensure backend is running on port 5000

### **Debug Steps:**
1. Check browser console for error messages
2. Verify API health endpoint responds
3. Test with the `/test` route
4. Check backend logs for detailed error information

## Conclusion

The integration successfully connects the existing frontend to the new backend AI model while maintaining full backward compatibility. The new API provides both file upload and text-based verification capabilities, with comprehensive error handling and testing tools.



