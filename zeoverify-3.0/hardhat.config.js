require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config(); // ✅ Make sure this is here

module.exports = {
  solidity: "0.8.20",
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL,   // ✅ must match .env
      accounts: [process.env.PRIVATE_KEY] // ✅ must match .env
    }
  }
};
