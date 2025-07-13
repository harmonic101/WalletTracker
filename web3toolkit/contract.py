from web3 import Web3
from typing import Any, Optional

# Deploy a contract (requires bytecode, ABI, deployer address, private key, and provider)
def deploy_contract(bytecode: str, abi: Any, deployer_address: str, private_key: str, provider_url: str) -> Optional[str]:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(deployer_address)
    tx = contract.constructor().build_transaction({
        'from': deployer_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price
    })
    signed = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return tx_hash.hex()

# Call a contract function (read-only)
def call_contract_function(contract_address: str, abi: Any, function_name: str, args: list, provider_url: str) -> Any:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    contract = w3.eth.contract(address=contract_address, abi=abi)
    func = getattr(contract.functions, function_name)
    return func(*args).call()

# Get contract ABI (requires external API, so here we just return None)
def get_contract_abi(contract_address: str, provider_url: str) -> Any:
    # This would require Etherscan or similar API, which needs an API key
    return None

# Listen to contract events (generator)
def listen_contract_events(contract_address: str, abi: Any, event_name: str, provider_url: str):
    w3 = Web3(Web3.HTTPProvider(provider_url))
    contract = w3.eth.contract(address=contract_address, abi=abi)
    event_filter = getattr(contract.events, event_name).create_filter(fromBlock='latest')
    while True:
        for event in event_filter.get_new_entries():
            yield event 