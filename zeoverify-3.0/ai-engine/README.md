# 🛡️ ZeoVerify 3.0 AI Engine - Refactored & Modular

A production-ready, modular AI engine for document verification with blockchain integration, designed to work offline without requiring Hugging Face authentication.

## 🚀 Features

- **🔍 OCR Processing**: Multi-format text extraction (images, PDFs, text files)
- **🤖 AI Classification**: Local models (TF-IDF + RandomForest, DistilBERT fallback)
- **🚨 Fraud Detection**: Rule-based fraud analysis engine
- **⛓️ Blockchain Integration**: Web3 integration for hash storage
- **📱 RESTful API**: Clean, documented endpoints
- **🔧 Modular Architecture**: Easy to maintain and extend
- **🌐 Offline Capable**: Works without internet connection

## 📁 Project Structure

```
ai-engine/
├── api/                          # Flask API modules
│   ├── __init__.py              # App factory
│   ├── routes.py                # API endpoints
│   └── uploads/                 # Temporary file storage
├── ml_model/                    # AI models and data
│   ├── model.pkl               # RandomForest classifier
│   ├── vectorizer.pkl          # TF-IDF vectorizer
│   ├── saved_model/            # DistilBERT model files
│   └── dataset.csv             # Training dataset
├── ocr.py                      # Text extraction module
├── classifier.py               # AI classification module
├── fraud_checker.py            # Fraud detection engine
├── blockchain_utils.py         # Web3 integration
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Git

### 1. Clone and Setup
```bash
# Navigate to ai-engine directory
cd zeoverify-3.0/ai-engine

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the `ai-engine` directory:

```env
# Flask Configuration
FLASK_ENV=development
PORT=5000
HOST=0.0.0.0

# Blockchain Configuration (Optional)
BLOCKCHAIN_RPC_URL=https://eth-goerli.g.alchemy.com/v2/YOUR_API_KEY
SMART_CONTRACT_ADDRESS=0x...
PRIVATE_KEY=your_private_key_here
CHAIN_ID=5
```

## 🚀 Running the Application

### Start the AI Engine
```bash
# From ai-engine directory
python app.py
```

The server will start on `http://localhost:5000`

### Production Deployment
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:main

# Or with environment variables
export FLASK_ENV=production
python app.py
```

## 📡 API Endpoints

### Health Check
```http
GET /health
```
Returns system status and model loading information.

### Document Verification (File Upload)
```http
POST /verify
Content-Type: multipart/form-data

file: [document file]
```
Processes uploaded document and returns comprehensive verification results.

**Response Format:**
```json
{
  "extracted_text": "Document text content...",
  "ml_document_type": "real_estate",
  "ml_confidence": 95.5,
  "fraud_risk": "low",
  "issues": [],
  "document_hash": "0x...",
  "blockchain_tx_hash": "0x...",
  "filename": "document.pdf"
}
```

### Text Verification
```http
POST /verify-text
Content-Type: application/json

{
  "text": "Document text content..."
}
```

### Blockchain Status
```http
GET /blockchain/status
```
Returns blockchain connection and network information.

## 🔧 Configuration

### Model Selection
The system automatically selects the best available model:

1. **TF-IDF + RandomForest** (default, fastest)
2. **DistilBERT** (fallback, more accurate)

### OCR Engines
Multiple OCR options with automatic fallback:

1. **EasyOCR** (best accuracy)
2. **Tesseract** (fallback)
3. **PDF processors** (pdfplumber, PyPDF2)

### Fraud Detection Rules
Configurable rules for:
- Suspicious keywords
- Missing essential fields
- Content quality issues
- Structural inconsistencies

## 🧪 Testing

### Test Individual Components
```bash
# Test OCR
python -c "from ocr import extract_text_from_file; print(extract_text_from_file('test.pdf'))"

# Test Classifier
python -c "from classifier import DocumentClassifier; c = DocumentClassifier(); print(c.is_loaded())"

# Test Fraud Detection
python -c "from fraud_checker import FraudDetector; f = FraudDetector(); print(f.analyze_document('test text'))"
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/health

# Test with sample file
curl -X POST -F "file=@test.pdf" http://localhost:5000/verify
```

## 🔒 Security Features

- **File Type Validation**: Only allowed file types accepted
- **Secure File Handling**: Temporary file storage with cleanup
- **Input Sanitization**: All inputs validated and sanitized
- **Error Handling**: Comprehensive error handling without information leakage
- **CORS Configuration**: Configurable cross-origin resource sharing

## 🌐 Blockchain Integration

### Supported Networks
- Ethereum Mainnet & Testnets
- Polygon
- Binance Smart Chain
- Local networks (Ganache, Hardhat)

### Smart Contract Interface
Basic ABI included for:
- `storeVerificationResult()`: Store verification results
- `getVerificationResult()`: Retrieve verification results

### Configuration
Set blockchain parameters in `.env`:
```env
BLOCKCHAIN_RPC_URL=https://...
SMART_CONTRACT_ADDRESS=0x...
PRIVATE_KEY=...
CHAIN_ID=1
```

## 🚧 Troubleshooting

### Common Issues

#### Model Loading Failed
```bash
# Check model files exist
ls ml_model/*.pkl
ls ml_model/saved_model/

# Verify dependencies
pip list | grep -E "(scikit-learn|joblib|torch)"
```

#### OCR Not Working
```bash
# Install system dependencies for Tesseract
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# macOS:
brew install tesseract

# Windows: Download from GitHub releases
```

#### Blockchain Connection Failed
```bash
# Check environment variables
echo $BLOCKCHAIN_RPC_URL
echo $SMART_CONTRACT_ADDRESS

# Verify network connectivity
curl -X POST -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  $BLOCKCHAIN_RPC_URL
```

### Logs and Debugging
```bash
# Enable debug logging
export FLASK_ENV=development
python app.py

# Check component status
curl http://localhost:5000/health
```

## 🔄 Extending the System

### Adding New Fraud Rules
```python
from fraud_checker import FraudDetector

detector = FraudDetector()
detector.add_custom_rule(
    rule_name="custom_pattern",
    pattern=r"\b(suspicious_word)\b",
    risk_score=0.7,
    description="Custom fraud detection rule"
)
```

### Adding New Document Types
```python
from classifier import DocumentClassifier

classifier = DocumentClassifier()
# Modify doc_type_map in classifier.py
```

### Custom Blockchain Integration
```python
from blockchain_utils import BlockchainManager

# Extend BlockchainManager class
# Add custom smart contract methods
# Implement additional networks
```

## 📊 Performance

### Model Performance
- **TF-IDF + RandomForest**: ~10-50ms inference time
- **DistilBERT**: ~100-500ms inference time
- **OCR Processing**: 1-10 seconds depending on file size

### Scalability
- Modular architecture allows horizontal scaling
- Stateless API design
- Configurable worker processes with Gunicorn

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs and error messages
3. Verify configuration and dependencies
4. Open an issue with detailed information

---

**Status**: ✅ **PRODUCTION READY** - Modular, scalable, and offline-capable AI engine!
