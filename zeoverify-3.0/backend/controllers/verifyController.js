const fs = require('fs');
const axios = require('axios');
const { ethers } = require('ethers');
const contractJson = require('../../blockchain/artifacts/contracts/ZeoDocumentVerifier.sol/ZeoDocumentVerifier.json');

// Connect to local blockchain
const provider = new ethers.JsonRpcProvider("http://127.0.0.1:8545");
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

// Create contract instance
const contract = new ethers.Contract(
  process.env.LOCAL_CONTRACT_ADDRESS,
  contractJson.abi,
  wallet
);

exports.verifyDocument = async (req, res) => {
  try {
    const file = req.file;
    if (!file) return res.status(400).json({ error: "File not provided" });

    console.log("📄 File received:", file.originalname);

    // Step 1: call AI engine
    console.log("🤖 Calling AI engine...");
    const aiResponse = await axios.post(process.env.FLASK_AI_URL, {
      filename: file.originalname
    });
    const aiResult = aiResponse.data; // e.g., { fraudScore: 0.2 }

    console.log("✅ AI result:", aiResult);

    // Step 2: write to blockchain
    console.log("⛓ Writing to blockchain...");
    const tx = await contract.storeVerificationResult(
      file.originalname,
      aiResult.fraudScore.toString()
    );
    await tx.wait();

    console.log("✅ Stored on blockchain:", tx.hash);

    res.json({
      message: "Document verified & stored on blockchain",
      txHash: tx.hash,
      aiResult
    });
  } catch (error) {
    console.error("❌ Error:", error);
    res.status(500).json({ error: "Something went wrong" });
  }
};
