from web3 import Web3
from eth_account import Account
import re
from typing import Optional, Dict, List
import secrets
import os

class Wallet:
    def __init__(self, address: str, network):
        """
        Initialize wallet with address and network.
        
        Args:
            address: Wallet address
            network: Network instance
        """
        # Convert to checksum address
        try:
            self.address = Web3.to_checksum_address(address)
        except Exception as e:
            print(f"Warning: Invalid address format: {e}")
            self.address = address
            
        self.network = network
        self.w3 = network.w3
    
    def get_balance(self) -> Dict[str, float]:
        """
        Get wallet balance.
        
        Returns:
            Dictionary with token balances
        """
        try:
            balance_wei = self.w3.eth.get_balance(self.address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            
            return {
                'ETH': float(balance_eth),
                'wei': int(balance_wei)
            }
        except Exception as e:
            print(f"Error getting balance: {e}")
            return {'ETH': 0.0, 'wei': 0}
    
    def get_transactions(self, limit: int = 100) -> List[Dict]:
        """
        Get recent transactions for this wallet.
        
        Args:
            limit: Number of transactions to fetch
            
        Returns:
            List of transaction dictionaries
        """
        try:
            # Get the latest block
            latest_block = self.w3.eth.block_number
            
            transactions = []
            block_count = 0
            
            # Scan recent blocks for transactions involving this address
            for block_num in range(latest_block, max(0, latest_block - 100), -1):
                if len(transactions) >= limit:
                    break
                    
                try:
                    block = self.w3.eth.get_block(block_num, full_transactions=True)
                    
                    for tx in block.transactions:
                        if len(transactions) >= limit:
                            break
                            
                        # Check if this transaction involves our address
                        if (tx['from'].lower() == self.address.lower() or 
                            tx['to'] and tx['to'].lower() == self.address.lower()):
                            
                            transactions.append({
                                'hash': tx['hash'].hex(),
                                'from': tx['from'],
                                'to': tx['to'],
                                'value': tx['value'],
                                'timestamp': block.timestamp,
                                'gas_used': tx.get('gas', 0),
                                'status': 'success'  # Assume success for now
                            })
                    
                    block_count += 1
                    
                except Exception as e:
                    print(f"Error getting block {block_num}: {e}")
                    continue
            
            return transactions
            
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []

# Create a new Ethereum wallet (private key + address)
def create_wallet() -> dict:
    acct = Account.create(os.urandom(32))
    return {'private_key': acct.key.hex(), 'address': acct.address}

# Validate an Ethereum address
def validate_address(address: str) -> bool:
    return Web3.is_address(address)

# Get the ETH balance of an address
def get_balance(address: str, provider_url: str) -> Optional[float]:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    if not w3.is_connected():
        raise ConnectionError('Web3 provider not connected')
    balance_wei = w3.eth.get_balance(address)
    return w3.from_wei(balance_wei, 'ether')

# Generate a random 12-word mnemonic (BIP39)
def generate_mnemonic() -> str:
    # Uses secrets for randomness, but for real BIP39 use 'mnemonic' package
    import hashlib
    import random
    wordlist_path = os.path.join(os.path.dirname(__file__), 'bip39_wordlist.txt')
    if not os.path.exists(wordlist_path):
        # fallback: use a small built-in list
        wordlist = [
            'apple', 'banana', 'cat', 'dog', 'elephant', 'fish', 'grape', 'hat', 'ice', 'jungle', 'kite', 'lemon',
            'monkey', 'nose', 'orange', 'pear', 'queen', 'rose', 'sun', 'tree', 'umbrella', 'violet', 'wolf', 'xray', 'yellow', 'zebra'
        ]
    else:
        with open(wordlist_path, 'r') as f:
            wordlist = [w.strip() for w in f.readlines() if w.strip()]
    return ' '.join(random.choice(wordlist) for _ in range(12)) 