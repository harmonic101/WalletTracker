from web3 import Web3
from eth_account import Account
from typing import Optional

def create_transaction(from_addr: str, to_addr: str, value: float, gas: int, gas_price: int, nonce: int, data: str = '') -> dict:
    return {
        'from': from_addr,
        'to': to_addr,
        'value': Web3.to_wei(value, 'ether'),
        'gas': gas,
        'gasPrice': gas_price,
        'nonce': nonce,
        'data': data
    }

def sign_transaction(tx: dict, private_key: str) -> str:
    signed = Account.sign_transaction(tx, private_key)
    return signed.rawTransaction.hex()

def send_transaction(signed_tx: str, provider_url: str) -> Optional[str]:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    if not w3.is_connected():
        raise ConnectionError('Web3 provider not connected')
    tx_hash = w3.eth.send_raw_transaction(bytes.fromhex(signed_tx.replace('0x', '')))
    return tx_hash.hex()

def get_transaction_status(tx_hash: str, provider_url: str) -> Optional[str]:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    if not w3.is_connected():
        raise ConnectionError('Web3 provider not connected')
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    return receipt.status if receipt else None

def estimate_gas(tx: dict, provider_url: str) -> int:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    if not w3.is_connected():
        raise ConnectionError('Web3 provider not connected')
    return w3.eth.estimate_gas(tx) 