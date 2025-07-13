from web3 import Web3
from typing import Optional, Any, List
import requests
from .config import ETHERSCAN_API_KEY, BSCSCAN_API_KEY, COVALENT_API_KEY, OPENSEA_API_KEY

# --- ENS (Ethereum Name Service) ---
def resolve_ens_name(ens_name: str, provider_url: str) -> Optional[str]:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    if not w3.is_connected() or not w3.ens:
        w3.ens = Web3.ENS.fromWeb3(w3)
    return w3.ens.address(ens_name)

def reverse_ens_lookup(address: str, provider_url: str) -> Optional[str]:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    if not w3.is_connected() or not w3.ens:
        w3.ens = Web3.ENS.fromWeb3(w3)
    return w3.ens.name(address)

# --- Gas Tools ---
def get_current_gas_price(provider_url: str) -> int:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    return w3.eth.gas_price

def estimate_total_fee(gas: int, provider_url: str) -> float:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    gas_price = w3.eth.gas_price
    return Web3.from_wei(gas * gas_price, 'ether')

# --- Nonce Management ---
def get_account_nonce(address: str, provider_url: str) -> int:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    return w3.eth.get_transaction_count(address)

# --- Token/NFT Utilities ---
def get_tokens_of_address(address: str, provider_url: str) -> List[str]:
    if not COVALENT_API_KEY:
        raise RuntimeError('Covalent API key is not set. Use set_api_keys() or set COVALENT_API_KEY env variable.')
    chain_id = 1  # Ethereum mainnet
    url = f'https://api.covalenthq.com/v1/{chain_id}/address/{address}/balances_v2/?key={COVALENT_API_KEY}'
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return [item['contract_address'] for item in data['data']['items'] if int(item['balance']) > 0]
    return []

def get_token_transfer_history(address: str, token_address: str, provider_url: str, chain: str = 'eth') -> Any:
    """
    chain: 'eth' for Ethereum, 'bsc' for Binance Smart Chain
    """
    if chain == 'bsc':
        api_key = BSCSCAN_API_KEY
        base_url = 'https://api.bscscan.com/api'
        if not api_key:
            raise RuntimeError('BscScan API key is not set. Use set_api_keys() or set BSCSCAN_API_KEY env variable.')
    else:
        api_key = ETHERSCAN_API_KEY
        base_url = 'https://api.etherscan.io/api'
        if not api_key:
            raise RuntimeError('Etherscan API key is not set. Use set_api_keys() or set ETHERSCAN_API_KEY env variable.')
    url = f'{base_url}?module=account&action=tokentx&address={address}&contractaddress={token_address}&sort=desc&apikey={api_key}'
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()['result']
    return []

def get_nfts_of_address(address: str, provider_url: str) -> List[Any]:
    if not COVALENT_API_KEY:
        raise RuntimeError('Covalent API key is not set. Use set_api_keys() or set COVALENT_API_KEY env variable.')
    chain_id = 1
    url = f'https://api.covalenthq.com/v1/{chain_id}/address/{address}/balances_v2/?nft=true&key={COVALENT_API_KEY}'
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return [item for item in data['data']['items'] if item.get('type') == 'nft']
    return []

def get_nft_metadata(token_address: str, token_id: int, provider_url: str) -> Any:
    if not OPENSEA_API_KEY:
        raise RuntimeError('OpenSea API key is not set. Use set_api_keys() or set OPENSEA_API_KEY env variable.')
    url = f'https://api.opensea.io/api/v1/asset/{token_address}/{token_id}/'
    headers = {'X-API-KEY': OPENSEA_API_KEY}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    return None

# --- Contract Helpers ---
def list_contract_functions(abi: Any) -> List[str]:
    return [item['name'] for item in abi if item.get('type') == 'function']

def get_contract_events(abi: Any) -> List[str]:
    return [item['name'] for item in abi if item.get('type') == 'event']

# --- Block/Tx Tools ---
def get_transactions_by_address(address: str, provider_url: str, start_block: int = 0, end_block: int = 99999999, chain: str = 'eth') -> Any:
    """
    chain: 'eth' for Ethereum, 'bsc' for Binance Smart Chain
    """
    if chain == 'bsc':
        api_key = BSCSCAN_API_KEY
        base_url = 'https://api.bscscan.com/api'
        if not api_key:
            raise RuntimeError('BscScan API key is not set. Use set_api_keys() or set BSCSCAN_API_KEY env variable.')
    else:
        api_key = ETHERSCAN_API_KEY
        base_url = 'https://api.etherscan.io/api'
        if not api_key:
            raise RuntimeError('Etherscan API key is not set. Use set_api_keys() or set ETHERSCAN_API_KEY env variable.')
    url = f'{base_url}?module=account&action=txlist&address={address}&startblock={start_block}&endblock={end_block}&sort=desc&apikey={api_key}'
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()['result']
    return []

def get_transactions_in_block(block_number: int, provider_url: str) -> Any:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    block = w3.eth.get_block(block_number, full_transactions=True)
    return block.transactions

# --- Network Health ---
def get_node_version(provider_url: str) -> str:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    return w3.client_version

def get_chain_id(provider_url: str) -> int:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    return w3.eth.chain_id

# --- Security & Analytics ---
def is_address_blacklisted(address: str) -> bool:
    blacklist = {'0x000000000000000000000000000000000000dead'}
    return address.lower() in blacklist

def is_contract_verified(contract_address: str, chain: str = 'eth') -> bool:
    """
    chain: 'eth' for Ethereum, 'bsc' for Binance Smart Chain
    """
    if chain == 'bsc':
        api_key = BSCSCAN_API_KEY
        base_url = 'https://api.bscscan.com/api'
        if not api_key:
            raise RuntimeError('BscScan API key is not set. Use set_api_keys() or set BSCSCAN_API_KEY env variable.')
    else:
        api_key = ETHERSCAN_API_KEY
        base_url = 'https://api.etherscan.io/api'
        if not api_key:
            raise RuntimeError('Etherscan API key is not set. Use set_api_keys() or set ETHERSCAN_API_KEY env variable.')
    url = f'{base_url}?module=contract&action=getsourcecode&address={contract_address}&apikey={api_key}'
    resp = requests.get(url)
    if resp.status_code == 200:
        result = resp.json()['result']
        return bool(result and result[0].get('SourceCode'))
    return False

def get_first_transaction_time(address: str, provider_url: str, chain: str = 'eth') -> Optional[str]:
    """
    chain: 'eth' for Ethereum, 'bsc' for Binance Smart Chain
    """
    if chain == 'bsc':
        api_key = BSCSCAN_API_KEY
        base_url = 'https://api.bscscan.com/api'
        if not api_key:
            raise RuntimeError('BscScan API key is not set. Use set_api_keys() or set BSCSCAN_API_KEY env variable.')
    else:
        api_key = ETHERSCAN_API_KEY
        base_url = 'https://api.etherscan.io/api'
        if not api_key:
            raise RuntimeError('Etherscan API key is not set. Use set_api_keys() or set ETHERSCAN_API_KEY env variable.')
    url = f'{base_url}?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}'
    resp = requests.get(url)
    if resp.status_code == 200:
        txs = resp.json()['result']
        if txs:
            return txs[0]['timeStamp']
    return None

def get_total_sent_received(address: str, provider_url: str, chain: str = 'eth') -> dict:
    """
    chain: 'eth' for Ethereum, 'bsc' for Binance Smart Chain
    """
    if chain == 'bsc':
        api_key = BSCSCAN_API_KEY
        base_url = 'https://api.bscscan.com/api'
        if not api_key:
            raise RuntimeError('BscScan API key is not set. Use set_api_keys() or set BSCSCAN_API_KEY env variable.')
    else:
        api_key = ETHERSCAN_API_KEY
        base_url = 'https://api.etherscan.io/api'
        if not api_key:
            raise RuntimeError('Etherscan API key is not set. Use set_api_keys() or set ETHERSCAN_API_KEY env variable.')
    url = f'{base_url}?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}'
    resp = requests.get(url)
    sent, received = 0, 0
    if resp.status_code == 200:
        txs = resp.json()['result']
        for tx in txs:
            if tx['from'].lower() == address.lower():
                sent += int(tx['value'])
            if tx['to'].lower() == address.lower():
                received += int(tx['value'])
    return {
        'sent_wei': sent,
        'received_wei': received,
        'sent_eth': Web3.from_wei(sent, 'ether'),
        'received_eth': Web3.from_wei(received, 'ether')
    } 