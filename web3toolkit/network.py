from web3 import Web3
from typing import Optional, Any

class Network:
    def __init__(self, network_name: str = "ethereum"):
        """
        Initialize network connection.
        
        Args:
            network_name: Network name (ethereum, bitcoin, etc.)
        """
        self.network_name = network_name
        
        # Updated provider URLs with working free endpoints
        self.providers = {
            "ethereum": "https://ethereum.publicnode.com",  # PublicNode - very reliable
            "ethereum_alt1": "https://rpc.ankr.com/eth",  # Ankr - alternative
            "ethereum_alt2": "https://eth.llamarpc.com",  # LlamaRPC - alternative
            "ethereum_alt3": "https://cloudflare-eth.com",  # Cloudflare - alternative
            "ethereum_testnet": "https://goerli.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
            "polygon": "https://polygon-rpc.com",
            "bsc": "https://bsc-dataseed.binance.org",
        }
        
        self.provider_url = self.providers.get(network_name, self.providers["ethereum"])
        self.w3 = Web3(Web3.HTTPProvider(self.provider_url))
        
        # Test connection and try alternatives if needed
        if not self.w3.is_connected():
            print(f"⚠️  Primary endpoint failed, trying alternatives...")
            for alt_name, alt_url in self.providers.items():
                if alt_name != network_name and "ethereum" in alt_name:
                    try:
                        print(f"🔄 Trying {alt_name}: {alt_url}")
                        self.w3 = Web3(Web3.HTTPProvider(alt_url))
                        if self.w3.is_connected():
                            print(f"✅ Connected using {alt_name}: {alt_url}")
                            self.provider_url = alt_url
                            break
                    except Exception as e:
                        print(f"❌ Failed {alt_name}: {e}")
                        continue
    
    def get_latest_block_number(self) -> int:
        """Get the latest block number."""
        try:
            return self.w3.eth.block_number
        except Exception as e:
            print(f"Error getting block number: {e}")
            return 0
    
    def is_connected(self) -> bool:
        """Check if connected to the network."""
        try:
            return self.w3.is_connected()
        except:
            return False
    
    def get_chain_id(self) -> int:
        """Get the chain ID."""
        try:
            return self.w3.eth.chain_id
        except Exception as e:
            print(f"Error getting chain ID: {e}")
            return 1

def get_network_status(provider_url: str) -> Any:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    return {
        'is_connected': w3.is_connected(),
        'client_version': w3.client_version,
        'chain_id': w3.eth.chain_id
    }

def get_block_number(provider_url: str) -> Optional[int]:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    return w3.eth.block_number

def get_block_details(block_number: int, provider_url: str) -> Any:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    return w3.eth.get_block(block_number)

def get_latest_transactions(provider_url: str, count: int = 10) -> Any:
    w3 = Web3(Web3.HTTPProvider(provider_url))
    latest = w3.eth.block_number
    block = w3.eth.get_block(latest, full_transactions=True)
    return block.transactions[:count] 