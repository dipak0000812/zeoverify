"""
Blockchain Utilities Module for ZeoVerify 3.0
Handles Web3 integration, smart contract interactions, and hash storage.
"""

import os
import logging
import hashlib
import json
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class BlockchainManager:
    """Manages blockchain interactions and smart contract operations."""
    
    def __init__(self):
        """Initialize blockchain connection and configuration."""
        self.connected = False
        self.web3 = None
        self.contract = None
        self.account = None
        self.network_info = {}
        
        # Configuration from environment
        self.rpc_url = os.getenv('BLOCKCHAIN_RPC_URL')
        self.contract_address = os.getenv('SMART_CONTRACT_ADDRESS')
        self.private_key = os.getenv('PRIVATE_KEY')
        self.chain_id = int(os.getenv('CHAIN_ID', '1'))
        
        # Try to connect to blockchain
        self._connect_to_blockchain()
    
    def _connect_to_blockchain(self):
        """Establish connection to blockchain network."""
        try:
            if not self.rpc_url:
                logger.warning("No blockchain RPC URL configured")
                return
            
            # Import Web3
            try:
                from web3 import Web3
            except ImportError:
                logger.warning("Web3 not installed. Install with: pip install web3")
                return
            
            # Connect to network
            self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
            
            if not self.web3.is_connected():
                logger.error("Failed to connect to blockchain network")
                return
            
            # Get network information
            self.network_info = {
                'chain_id': self.web3.eth.chain_id,
                'block_number': self.web3.eth.block_number,
                'gas_price': self.web3.eth.gas_price,
                'network_name': self._get_network_name(self.web3.eth.chain_id)
            }
            
            # Setup account if private key is provided
            if self.private_key:
                try:
                    self.account = self.web3.eth.account.from_key(self.private_key)
                    logger.info(f"Account configured: {self.account.address}")
                except Exception as e:
                    logger.error(f"Failed to setup account: {e}")
            
            # Setup smart contract if address is provided
            if self.contract_address:
                self._setup_smart_contract()
            
            self.connected = True
            logger.info(f"✅ Connected to {self.network_info.get('network_name', 'blockchain')}")
            
        except Exception as e:
            logger.error(f"Failed to connect to blockchain: {e}")
            self.connected = False
    
    def _setup_smart_contract(self):
        """Setup smart contract interface."""
        try:
            if not self.web3 or not self.contract_address:
                return
            
            # Basic smart contract ABI for document verification
            # This is a simplified ABI - you can extend it based on your actual contract
            basic_abi = [
                {
                    "inputs": [
                        {"name": "documentHash", "type": "string"},
                        {"name": "documentType", "type": "string"},
                        {"name": "fraudRisk", "type": "string"},
                        {"name": "confidence", "type": "uint256"}
                    ],
                    "name": "storeVerificationResult",
                    "outputs": [{"name": "", "type": "bool"}],
                    "stateMutability": "nonpayable",
                    "type": "function"
                },
                {
                    "inputs": [{"name": "documentHash", "type": "string"}],
                    "name": "getVerificationResult",
                    "outputs": [
                        {"name": "documentType", "type": "string"},
                        {"name": "fraudRisk", "type": "string"},
                        {"name": "confidence", "type": "uint256"},
                        {"name": "timestamp", "type": "uint256"}
                    ],
                    "stateMutability": "view",
                    "type": "function"
                }
            ]
            
            # Create contract instance
            self.contract = self.web3.eth.contract(
                address=self.contract_address,
                abi=basic_abi
            )
            
            logger.info(f"Smart contract interface ready: {self.contract_address}")
            
        except Exception as e:
            logger.error(f"Failed to setup smart contract: {e}")
    
    def _get_network_name(self, chain_id: int) -> str:
        """Get human-readable network name from chain ID."""
        network_names = {
            1: "Ethereum Mainnet",
            3: "Ropsten Testnet",
            4: "Rinkeby Testnet",
            5: "Goerli Testnet",
            42: "Kovan Testnet",
            56: "Binance Smart Chain",
            137: "Polygon",
            80001: "Mumbai Testnet",
            1337: "Local Ganache",
            31337: "Local Hardhat"
        }
        return network_names.get(chain_id, f"Unknown Network ({chain_id})")
    
    def is_connected(self) -> bool:
        """Check if connected to blockchain."""
        return self.connected and self.web3 and self.web3.is_connected()
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get current network information."""
        if not self.is_connected():
            return {"connected": False, "error": "Not connected to blockchain"}
        
        try:
            return {
                "connected": True,
                "network_name": self.network_info.get('network_name', 'Unknown'),
                "chain_id": self.web3.eth.chain_id,
                "block_number": self.web3.eth.block_number,
                "gas_price": self.web3.eth.gas_price,
                "account_address": self.account.address if self.account else None
            }
        except Exception as e:
            logger.error(f"Error getting network info: {e}")
            return {"connected": False, "error": str(e)}
    
    def store_verification_result(self, document_hash: str, document_type: str, 
                                fraud_risk: str, confidence: float) -> Optional[str]:
        """
        Store verification result on blockchain.
        
        Args:
            document_hash: SHA256 hash of the document
            document_type: Type of document (real_estate, fake, invalid)
            fraud_risk: Risk level (low, medium, high)
            confidence: Confidence score (0.0 to 1.0)
            
        Returns:
            Transaction hash if successful, None otherwise
        """
        if not self.is_connected():
            logger.warning("Cannot store result: not connected to blockchain")
            return None
        
        if not self.contract or not self.account:
            logger.warning("Cannot store result: smart contract or account not configured")
            return None
        
        try:
            # Convert confidence to integer (multiply by 100 for precision)
            confidence_int = int(confidence * 100)
            
            # Build transaction
            transaction = self.contract.functions.storeVerificationResult(
                document_hash,
                document_type,
                fraud_risk,
                confidence_int
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.web3.eth.get_transaction_count(self.account.address),
                'gas': 200000,  # Adjust gas limit as needed
                'gasPrice': self.web3.eth.gas_price
            })
            
            # Sign and send transaction
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                logger.info(f"✅ Verification result stored on blockchain: {tx_hash.hex()}")
                return tx_hash.hex()
            else:
                logger.error(f"❌ Transaction failed: {tx_hash.hex()}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to store verification result: {e}")
            return None
    
    def get_verification_result(self, document_hash: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve verification result from blockchain.
        
        Args:
            document_hash: SHA256 hash of the document
            
        Returns:
            Verification result dictionary or None if not found
        """
        if not self.is_connected() or not self.contract:
            return None
        
        try:
            result = self.contract.functions.getVerificationResult(document_hash).call()
            
            return {
                'document_type': result[0],
                'fraud_risk': result[1],
                'confidence': result[2] / 100.0,  # Convert back to 0-1 scale
                'timestamp': result[3],
                'blockchain_verified': True
            }
            
        except Exception as e:
            logger.error(f"Failed to retrieve verification result: {e}")
            return None
    
    def verify_document_hash(self, document_hash: str) -> bool:
        """
        Check if document hash exists on blockchain.
        
        Args:
            document_hash: SHA256 hash to verify
            
        Returns:
            True if hash exists, False otherwise
        """
        result = self.get_verification_result(document_hash)
        return result is not None
    
    def get_storage_cost_estimate(self) -> Dict[str, Any]:
        """Get estimated cost for storing verification result."""
        if not self.is_connected():
            return {"error": "Not connected to blockchain"}
        
        try:
            gas_price = self.web3.eth.gas_price
            estimated_gas = 200000  # Estimated gas for storeVerificationResult
            
            # Convert to ETH (assuming 18 decimals)
            gas_cost_wei = gas_price * estimated_gas
            gas_cost_eth = self.web3.from_wei(gas_cost_wei, 'ether')
            
            return {
                "estimated_gas": estimated_gas,
                "gas_price_wei": gas_price,
                "gas_price_gwei": self.web3.from_wei(gas_price, 'gwei'),
                "total_cost_wei": gas_cost_wei,
                "total_cost_eth": gas_cost_eth,
                "currency": "ETH"
            }
            
        except Exception as e:
            logger.error(f"Error estimating storage cost: {e}")
            return {"error": str(e)}
    
    def disconnect(self):
        """Disconnect from blockchain network."""
        if self.web3:
            self.web3 = None
        self.connected = False
        self.contract = None
        self.account = None
        logger.info("Disconnected from blockchain network")
