# 🏠 ZeoVerify 3.0 - AI-Powered Document Verification System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-19.1.0-61dafb.svg)](https://reactjs.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![Blockchain](https://img.shields.io/badge/Blockchain-Hardhat-orange.svg)](https://hardhat.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **A cutting-edge blockchain-based digital certificate verification system with AI-powered fraud detection and real-time document analysis.**

## ✨ **Features**

- 🤖 **AI-Powered Verification** - Machine learning models for document authenticity detection
- 📄 **Multi-Format Support** - PDF, JPEG, PNG document processing
- 🔒 **Blockchain Integration** - Immutable verification records on Ethereum
- 🌐 **Modern Web Interface** - React-based responsive frontend
- 📊 **Real-Time Analysis** - Instant fraud risk assessment and confidence scoring
- 🔍 **Advanced OCR** - Text extraction from various document formats
- 📱 **Responsive Design** - Works seamlessly on all devices
- 🚀 **Production Ready** - Comprehensive error handling and logging

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI Engine     │
│   (React)       │◄──►│   (Node.js)     │◄──►│   (Flask)       │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Blockchain    │
                       │   (Hardhat)     │
                       │                 │
                       └─────────────────┘
```

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- Node.js 16+ and npm
- Git
- Modern web browser

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/zeoverify-3.0.git
cd zeoverify-3.0
```

### **2. Backend Setup (AI Engine)**
```bash
# Navigate to the AI engine directory
cd ai-engine/api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask API
python app_simple.py
```

The AI backend will start on `http://localhost:5000`

### **3. Frontend Setup**
```bash
# Navigate to the frontend directory
cd ../../frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will start on `http://localhost:5173`

### **4. Blockchain Setup (Optional)**
```bash
# Navigate to the blockchain directory
cd ../blockchain

# Install dependencies
npm install

# Start local blockchain
npx hardhat node

# Deploy contracts (in another terminal)
npx hardhat run scripts/deploy.js --network localhost
```

## 🔧 **API Endpoints**

### **AI Engine (Flask)**
- `GET /health` - Health check and model status
- `POST /verify` - Text-based document verification
- `POST /api/verify` - File upload verification (frontend compatible)
- `POST /verify-simple` - Simple verification without confidence

### **Backend (Node.js)**
- `GET /api/health` - Backend health check
- `POST /api/verify` - Document verification endpoint
- `GET /api/verify/history` - Verification history

## 🧪 **Testing**

### **Test the API**
```bash
cd ai-engine/api
python test_improvements.py
```

### **Test Frontend Integration**
1. Start backend: `python app_simple.py` (in ai-engine/api)
2. Start frontend: `npm run dev` (in frontend)
3. Navigate to `http://localhost:5173`
4. Go to Upload page and test file upload
5. Check `/test` route for API testing interface

## 📁 **Project Structure**

```
zeoverify-3.0/
├── 📁 ai-engine/                 # AI and ML components
│   ├── 📁 api/                   # Flask API server
│   │   ├── app_simple.py        # Main API application
│   │   ├── requirements.txt     # Python dependencies
│   │   └── test_improvements.py # API testing suite
│   └── 📁 ml_model/             # Machine learning models
│       ├── model.pkl            # Trained RandomForest model
│       ├── vectorizer.pkl       # TF-IDF vectorizer
│       └── predict_fixed.py     # Prediction functions
├── 📁 frontend/                  # React web application
│   ├── 📁 src/
│   │   ├── 📁 components/       # React components
│   │   ├── 📁 pages/            # Page components
│   │   └── 📁 services/         # API service functions
│   └── package.json
├── 📁 backend/                   # Node.js backend server
├── 📁 blockchain/                # Smart contracts and blockchain
├── 📁 docs/                      # Documentation and sample documents
└── README.md                     # This file
```

## 🤖 **AI Model Details**

### **Current Model**
- **Algorithm**: TF-IDF + Random Forest Classifier
- **Features**: Text-based document classification
- **Classes**: `real_estate`, `fake`, `invalid`
- **Accuracy**: High confidence scoring for document authenticity

### **Training Data**
- Real estate documents (agreements, deeds, certificates)
- Fraudulent document samples
- Invalid document patterns

## 🔒 **Security Features**

- File type validation
- File size limits (5MB)
- Input sanitization
- CORS protection
- Comprehensive error handling
- Request logging and monitoring

## 🌟 **What's New in 3.0**

- ✅ **Improved AI Engine** - Clean, focused Flask API
- ✅ **Real Text Extraction** - PDF and image processing
- ✅ **Enhanced Frontend** - Modern, responsive design
- ✅ **Better Error Handling** - User-friendly error messages
- ✅ **Production Logging** - Request/response monitoring
- ✅ **File Validation** - Type and size restrictions
- ✅ **Comprehensive Testing** - Automated test suite

## 🚧 **Roadmap**

- [ ] **OCR Integration** - Tesseract-based text extraction
- [ ] **Multi-Language Support** - International document verification
- [ ] **Advanced Fraud Detection** - Pattern recognition algorithms
- [ ] **Mobile App** - React Native application
- [ ] **Cloud Deployment** - AWS/Azure integration
- [ ] **API Rate Limiting** - Production-grade security
- [ ] **Real-time Notifications** - WebSocket integration

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **How to Contribute**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Machine Learning**: Scikit-learn, NumPy, Joblib
- **Web Framework**: Flask, React, Vite
- **Blockchain**: Hardhat, Solidity
- **Styling**: Tailwind CSS
- **Testing**: Comprehensive test suite

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/yourusername/zeoverify-3.0/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/zeoverify-3.0/discussions)
- **Email**: your.email@example.com

## ⭐ **Star the Project**

If you find this project helpful, please give it a star on GitHub!

---

**Built with ❤️ by [Your Name]**

*ZeoVerify 3.0 - Making document verification secure, fast, and reliable.*
