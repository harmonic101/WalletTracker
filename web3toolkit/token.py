from web3 import Web3
from eth_account import Account
from typing import Optional, Any
import json

# Standard ERC-20 ABI (minimal)
ERC20_ABI = json.loads('[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"type":"function"}]')

def get_token_balance(address: str, token_address: str, provider_url: str) -> Optional[float]:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
    decimals = contract.functions.decimals().call()
    balance = contract.functions.balanceOf(address).call()
    return balance / (10 ** decimals)

def transfer_token(from_addr: str, to_addr: str, amount: float, token_address: str, private_key: str, provider_url: str) -> Optional[str]:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
    decimals = contract.functions.decimals().call()
    nonce = w3.eth.get_transaction_count(from_addr)
    tx = contract.functions.transfer(to_addr, int(amount * (10 ** decimals))).build_transaction({
        'from': from_addr,
        'nonce': nonce,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price
    })
    signed = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return tx_hash.hex()

def approve_token(owner_addr: str, spender_addr: str, amount: float, token_address: str, private_key: str, provider_url: str) -> Optional[str]:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
    decimals = contract.functions.decimals().call()
    nonce = w3.eth.get_transaction_count(owner_addr)
    tx = contract.functions.approve(spender_addr, int(amount * (10 ** decimals))).build_transaction({
        'from': owner_addr,
        'nonce': nonce,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price
    })
    signed = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return tx_hash.hex()

def get_token_metadata(token_address: str, provider_url: str) -> Any:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
    return {
        'name': contract.functions.name().call(),
        'symbol': contract.functions.symbol().call(),
        'decimals': contract.functions.decimals().call(),
        'address': token_address
    } 