# 🔧 Zeoverify Setup & Connection Guide

## 📋 Prerequisites

1. **Node.js** (v16+)
2. **Python** (v3.8+)
3. **Tesseract OCR** installed
4. **Hardhat** blockchain running

## 🚀 Quick Start

### 1. Start Blockchain (Hardhat)
```bash
cd blockchain
npm install
npx hardhat compile
npx hardhat node  # Keep this running in terminal 1
```

### 2. Deploy Smart Contract
```bash
# In a new terminal
cd blockchain
npx hardhat run scripts/deploy.js --network localhost
# Copy the contract address and update backend/.env
```

### 3. Setup Environment Variables

Create `backend/.env` file:
```env
# Blockchain Configuration
PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3
RPC_URL=http://127.0.0.1:8545

# AI Engine URL
AI_ENGINE_URL=http://127.0.0.1:5001

# Server Configuration
PORT=5000
NODE_ENV=development
```

### 4. Install Dependencies

**Backend:**
```bash
cd backend
npm install
```

**Frontend:**
```bash
cd frontend
npm install
```

**AI Engine:**
```bash
cd ai-engine
pip install -r requirements.txt
```

### 5. Start All Services

**Option A: Manual Start**
```bash
# Terminal 1: AI Engine (Port 5001)
cd ai-engine
python app.py

# Terminal 2: Backend (Port 5000)
cd backend
npm start

# Terminal 3: Frontend (Port 5173)
cd frontend
npm run dev
```

**Option B: Auto Start**
```bash
# From project root
node start-all.js
```

## 🔗 Service Connections

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| Frontend | 5173 | http://localhost:5173 | React UI |
| Backend | 5000 | http://localhost:5000 | Node.js API |
| AI Engine | 5001 | http://localhost:5001 | Flask AI Service |
| Blockchain | 8545 | http://localhost:8545 | Hardhat Network |

## 🔄 Data Flow

1. **Frontend** → **Backend** (`POST /api/verify`)
2. **Backend** → **AI Engine** (`POST /verify-document`)
3. **AI Engine** → **Backend** (returns OCR + fraud analysis)
4. **Backend** → **Blockchain** (stores document hash)
5. **Backend** → **Frontend** (returns complete results)

## 🧪 Testing the Connection

1. Open http://localhost:5173
2. Upload a document (PDF, image)
3. Check console logs in each terminal
4. Verify blockchain transaction on http://localhost:8545

## 🐛 Troubleshooting

### Port Conflicts
- AI Engine: Change port in `ai-engine/app.py`
- Backend: Change port in `backend/index.js`
- Frontend: Change port in `frontend/vite.config.js`

### Blockchain Issues
- Ensure Hardhat node is running
- Check contract deployment
- Verify private key and contract address

### AI Engine Issues
- Install Tesseract OCR
- Check Python dependencies
- Verify file upload permissions

### CORS Issues
- Backend has CORS enabled
- Check frontend API calls
- Verify service URLs 