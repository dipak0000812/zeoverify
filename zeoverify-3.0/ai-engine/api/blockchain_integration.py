#!/usr/bin/env python3
"""
Example blockchain integration module for the Certificate Verification API.
This module demonstrates how to integrate verification results with blockchain storage.
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class BlockchainIntegration:
    """
    Example blockchain integration class for storing verification results.
    This is a placeholder implementation that can be extended with actual blockchain libraries.
    """
    
    def __init__(self, blockchain_config: Optional[Dict[str, Any]] = None):
        """Initialize blockchain integration."""
        self.config = blockchain_config or {}
        self.verification_history = []  # In-memory storage for demo
        
    def generate_document_hash(self, certificate_text: str) -> str:
        """Generate SHA-256 hash of certificate text."""
        return hashlib.sha256(certificate_text.encode('utf-8')).hexdigest()
    
    def store_verification_result(self, 
                                certificate_text: str, 
                                verification_result: Dict[str, Any],
                                user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Store verification result on blockchain.
        
        Args:
            certificate_text: The original certificate text
            verification_result: Result from the ML model
            user_id: Optional user identifier
            
        Returns:
            Dictionary containing transaction details
        """
        # Generate document hash
        document_hash = self.generate_document_hash(certificate_text)
        
        # Create verification record
        verification_record = {
            'document_hash': document_hash,
            'verification_timestamp': datetime.utcnow().isoformat(),
            'verification_result': verification_result,
            'user_id': user_id,
            'blockchain_tx_id': f"tx_{int(time.time())}_{hash(document_hash) % 10000}"
        }
        
        # Store in blockchain (placeholder implementation)
        self._store_on_blockchain(verification_record)
        
        # Add to local history for demo
        self.verification_history.append(verification_record)
        
        return {
            'success': True,
            'document_hash': document_hash,
            'transaction_id': verification_record['blockchain_tx_id'],
            'timestamp': verification_record['verification_timestamp']
        }
    
    def verify_document_hash(self, certificate_text: str) -> Optional[Dict[str, Any]]:
        """
        Verify if a document hash exists on blockchain.
        
        Args:
            certificate_text: The certificate text to verify
            
        Returns:
            Verification record if found, None otherwise
        """
        document_hash = self.generate_document_hash(certificate_text)
        
        # Search blockchain for document hash (placeholder implementation)
        for record in self.verification_history:
            if record['document_hash'] == document_hash:
                return record
        
        return None
    
    def get_verification_history(self, limit: int = 10) -> list:
        """Get recent verification history."""
        return self.verification_history[-limit:]
    
    def _store_on_blockchain(self, verification_record: Dict[str, Any]) -> bool:
        """
        Store verification record on actual blockchain.
        This is a placeholder implementation.
        
        In a real implementation, you would:
        1. Connect to Ethereum/other blockchain
        2. Call smart contract function
        3. Wait for transaction confirmation
        4. Return transaction hash
        """
        # Placeholder for actual blockchain storage
        print(f"🔗 Storing on blockchain: {verification_record['blockchain_tx_id']}")
        
        # Example Ethereum integration (commented out)
        """
        from web3 import Web3
        
        # Connect to Ethereum network
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'))
        
        # Load smart contract
        contract_address = '0x...'
        contract_abi = [...]
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        
        # Prepare transaction
        tx = contract.functions.storeVerification(
            verification_record['document_hash'],
            json.dumps(verification_record['verification_result']),
            verification_record['verification_timestamp']
        ).build_transaction({
            'from': w3.eth.accounts[0],
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(w3.eth.accounts[0])
        })
        
        # Sign and send transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for confirmation
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt['transactionHash'].hex()
        """
        
        return True

# Example usage with the API
def integrate_with_api():
    """Example of how to integrate blockchain with the API."""
    
    # Initialize blockchain integration
    blockchain = BlockchainIntegration()
    
    # Example verification result from API
    verification_result = {
        'status': 'real_estate',
        'confidence': 0.95,
        'probabilities': [0.95, 0.03, 0.02]
    }
    
    certificate_text = "This is a real estate document with property details and ownership information."
    
    # Store verification result on blockchain
    result = blockchain.store_verification_result(
        certificate_text=certificate_text,
        verification_result=verification_result,
        user_id="user123"
    )
    
    print("Blockchain Integration Result:")
    print(json.dumps(result, indent=2))
    
    # Verify document hash
    verification_record = blockchain.verify_document_hash(certificate_text)
    if verification_record:
        print("\nDocument Verification Record:")
        print(json.dumps(verification_record, indent=2))
    
    return result

if __name__ == "__main__":
    integrate_with_api()
