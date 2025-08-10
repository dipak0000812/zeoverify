# Certificate Verification API

A Flask-based REST API for verifying digital certificates using a trained DistilBERT transformer model. This API integrates with the blockchain-based digital certificate verification system.

## Features

- **Certificate Verification**: Classify certificates as `real_estate`, `fake`, or `invalid`
- **Confidence Scoring**: Returns prediction confidence scores
- **Health Monitoring**: Built-in health check endpoint
- **Error Handling**: Comprehensive error handling for invalid inputs
- **CORS Support**: Cross-origin resource sharing enabled
- **Modular Design**: Prepared for blockchain integration

## API Endpoints

### Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Response**: 
```json
{
  "status": "running",
  "model_loaded": true
}
```

### Certificate Verification
- **URL**: `/verify`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
```json
{
  "certificate_text": "Your certificate text here..."
}
```
- **Response**:
```json
{
  "status": "real_estate",
  "confidence": 0.95,
  "message": "Certificate classified as real_estate with 95.00% confidence"
}
```

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup

1. **Navigate to the API directory**:
```bash
cd zeoverify-3.0/ai-engine/api
```

2. **Create and activate virtual environment**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Verify model files exist**:
```bash
# Check that the model files are present
ls ../ml_model/saved_model/
# Should show: config.json, model.safetensors, tokenizer.json, vocab.txt
```

## Running the API

### Development Mode
```bash
python app.py
```

### Production Mode
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables
- `PORT`: Port number (default: 5000)
- `FLASK_ENV`: Set to 'development' for debug mode

## Testing the API

### Using the Test Script
```bash
python test_api.py
```

### Manual Testing with curl

1. **Health Check**:
```bash
curl http://localhost:5000/health
```

2. **Certificate Verification**:
```bash
curl -X POST http://localhost:5000/verify \
  -H "Content-Type: application/json" \
  -d '{
    "certificate_text": "This is a real estate document with property details and ownership information."
  }'
```

## Model Information

The API uses a trained DistilBERT model for sequence classification with the following characteristics:

- **Model Type**: DistilBERT for Sequence Classification
- **Classes**: 3 (real_estate, fake, invalid)
- **Max Sequence Length**: 512 tokens
- **Model Location**: `../ml_model/saved_model/`

## Integration with Blockchain System

The API is designed to be easily integrated with the blockchain storage system:

### Modular Architecture
- `CertificateVerifier` class can be imported and used in other modules
- Model loading is separated from API logic
- Prediction results include confidence scores for blockchain validation

### Future Integration Points
1. **Blockchain Storage**: Store verification results on blockchain
2. **Hash Verification**: Verify document hashes against blockchain records
3. **Audit Trail**: Log all verification attempts for transparency
4. **Smart Contracts**: Integrate with Ethereum smart contracts for automated verification

## Troubleshooting

### Common Issues

1. **Model Loading Error**:
   - Ensure all model files exist in `../ml_model/saved_model/`
   - Check file permissions
   - Verify Python environment has required packages

2. **Port Already in Use**:
   - Change port in environment variable: `export PORT=5001`
   - Or kill existing process: `lsof -ti:5000 | xargs kill -9`

## Performance Considerations

- **Model Loading**: Model is loaded once at startup
- **Prediction Speed**: ~100-500ms per prediction depending on text length
- **Memory Usage**: ~500MB for model + dependencies
- **Concurrent Requests**: Handle multiple requests simultaneously
