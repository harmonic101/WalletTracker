from web3 import Web3
import re
from datetime import datetime

# Convert hex string to int
def hex_to_int(hex_str: str) -> int:
    return int(hex_str, 16)

# Convert int to hex string
def int_to_hex(value: int) -> str:
    return hex(value)

# Convert string to hex string
def str_to_hex(s: str) -> str:
    return s.encode().hex()

# Convert hex string to string
def hex_to_str(hex_str: str) -> str:
    return bytes.fromhex(hex_str.replace('0x', '')).decode(errors='ignore')

# Convert timestamp to datetime
def timestamp_to_datetime(ts: int) -> datetime:
    return datetime.utcfromtimestamp(ts)

# Convert datetime to timestamp
def datetime_to_timestamp(dt: datetime) -> int:
    return int(dt.timestamp())

# Validate IPFS hash (Qm...)
def validate_ipfs_hash(ipfs_hash: str) -> bool:
    # Simple IPFS hash validation (Qm...)
    return bool(re.match(r'Qm[1-9A-HJ-NP-Za-km-z]{44}', ipfs_hash))

# Convert address to checksum address
def to_checksum_address(address: str) -> str:
    return Web3.to_checksum_address(address)

# Keccak256 hash of data
def keccak256(data: bytes) -> str:
    return Web3.keccak(data).hex() 