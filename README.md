# 🛡️ Zeoverify — Decentralized Document Verification

Document verification system powered by:
- 🧠 AI Engine (Flask, OCR, fraud detection)
- 🔗 Blockchain (Hardhat, Solidity)
- 🌐 Node.js backend (Express, ethers.js)
- 💻 React frontend (Tailwind CSS)

---

## 📦 Project Structure

zeoverify-3.0/
├── frontend/ # React app
├── backend/ # Node.js backend API
├── ai-engine/ # Flask AI Engine (OCR + fraud)
├── blockchain/ # Hardhat smart contracts
└── README.md
```

---

## 🛠 How It Works (Flow)

1. User uploads document → frontend sends to backend  
2. Backend:
   - Calls AI Engine → get extracted text & fraud status
   - Stores file hash on blockchain
3. Backend sends result to frontend
4. Frontend shows extracted text, fraud status & hash

---

## ⚙️ Setup Guide

> Clone repo first:
```bash
git clone https://github.com/dipak0000812/zeoverify.git
cd zeoverify-3.0


📌 AI Engine
cd ai-engine
pip install -r requirements.txt
python app.py
Install Tesseract OCR & set path in ocr_engine.py:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

📌 Blockchain (Hardhat)
cd blockchain
npm install
npx hardhat compile
npx hardhat node   # start local blockchain (http://127.0.0.1:8545)
npx hardhat run scripts/deploy.js --network localhost

📌 Backend (Node.js)
cd backend
npm install

📌 Frontend (React)
cd frontend
npm install
npm start

🔗 API Flow
Frontend → POST /api/verify → backend

Backend → AI Engine (POST /verify-document)

AI Engine → returns extracted text & fraud

Backend → stores hash on blockchain

Backend → sends final JSON:
