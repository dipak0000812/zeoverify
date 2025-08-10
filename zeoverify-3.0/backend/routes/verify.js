const express = require('express');
const router = express.Router();
const multer = require('multer');
const axios = require('axios');
const { ethers } = require('ethers');
const FormData = require('form-data');

const upload = multer();

// In-memory storage for verification history (replace with database in production)
let verificationHistory = [];

// ✅ Everything inside this route:
router.post('/', upload.single('file'), async (req, res) => {
  try {
    const file = req.file;
    if (!file) return res.status(400).json({ error: 'No file uploaded' });

    // 🧰 Prepare form-data
    const form = new FormData();
    form.append('file', file.buffer, file.originalname);

    // 📡 Call AI engine
    const aiResponse = await axios.post(
      'http://127.0.0.1:5001/verify-document',
      form,
      { headers: form.getHeaders() }
    );

    const { extracted_text, fraud_issues, fraud_risk, doc_type_ml, doc_type_rule } = aiResponse.data;

    // 🔗 Store hash on blockchain
    const fileHash = ethers.keccak256(file.buffer);
    const provider = new ethers.JsonRpcProvider(process.env.RPC_URL || 'http://127.0.0.1:8545');
    const privateKey = process.env.PRIVATE_KEY || '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80';
    const contractAddress = process.env.CONTRACT_ADDRESS || '0x5FbDB2315678afecb367f032d93F642f64180aa3';
    
    // Contract ABI for ZeoDocumentVerifier
    const contractABI = [
      "function verifyDocument(bytes32 docHash) public",
      "function isVerified(bytes32 docHash) public view returns (bool)",
      "event DocumentVerified(bytes32 indexed docHash, address indexed verifier)"
    ];

    const wallet = new ethers.Wallet(privateKey, provider);
    const contract = new ethers.Contract(contractAddress, contractABI, wallet);

    try {
      await contract.verifyDocument(fileHash);
      console.log('✅ Document hash stored on blockchain:', fileHash);
    } catch (blockchainError) {
      console.error('⚠️ Blockchain error:', blockchainError.message);
      // Continue with response even if blockchain fails
    }

    // 📝 Store verification record
    const verificationRecord = {
      id: Date.now(),
      filename: file.originalname,
      verifiedAt: new Date().toISOString(),
      fraudRisk: getFraudRiskPercentage(fraud_risk),
      result: fraud_risk === 'Low' ? 'Genuine' : 'Invalid',
      documentType: doc_type_ml || doc_type_rule,
      extractedText: extracted_text,
      fraudIssues: fraud_issues || [],
      fileHash: fileHash
    };

    verificationHistory.unshift(verificationRecord); // Add to beginning of array

    res.json({
      filename: file.originalname,
      verified_at: verificationRecord.verifiedAt,
      fraud_risk_percentage: verificationRecord.fraudRisk,
      result: verificationRecord.result,
      document_type: verificationRecord.documentType,
      extracted_text,
      fraud_issues,
      fraud_risk,
      doc_type_ml,
      doc_type_rule,
      file_hash: fileHash,
      verification_id: verificationRecord.id
    });
  } catch (error) {
    console.error('[ERROR]:', error.message);
    res.status(500).json({ 
      error: 'Something went wrong',
      details: error.message 
    });
  }
});

// Get verification history
router.get('/history', (req, res) => {
  try {
    res.json({
      success: true,
      data: verificationHistory,
      total: verificationHistory.length
    });
  } catch (error) {
    console.error('[ERROR]:', error.message);
    res.status(500).json({ 
      error: 'Failed to fetch verification history',
      details: error.message 
    });
  }
});

// Get specific verification by ID
router.get('/history/:id', (req, res) => {
  try {
    const verification = verificationHistory.find(v => v.id === parseInt(req.params.id));
    if (!verification) {
      return res.status(404).json({ error: 'Verification not found' });
    }
    res.json({
      success: true,
      data: verification
    });
  } catch (error) {
    console.error('[ERROR]:', error.message);
    res.status(500).json({ 
      error: 'Failed to fetch verification',
      details: error.message 
    });
  }
});

// Helper function to convert fraud risk to percentage
const getFraudRiskPercentage = (risk) => {
  if (risk === 'Low') return 25;
  if (risk === 'Medium') return 60;
  if (risk === 'High') return 90;
  return 50;
};

module.exports = router;
