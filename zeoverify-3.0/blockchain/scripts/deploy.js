const { ethers } = require("hardhat");

async function main() {
  console.log("🚀 Deploying ZeoDocumentVerifier...");

  const ZeoDocumentVerifier = await ethers.getContractFactory("ZeoDocumentVerifier");
  const verifier = await ZeoDocumentVerifier.deploy();

  await verifier.waitForDeployment(); // 🔄 This replaces `verifier.deployed()`

  console.log("✅ Deployed to:", verifier.target); // 🔁 Use `.target` for the deployed address
}

main().catch((error) => {
  console.error("❌ Deployment failed:", error);
  process.exitCode = 1;
});
