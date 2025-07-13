import os

ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY')
BSCSCAN_API_KEY = os.environ.get('BSCSCAN_API_KEY')
COVALENT_API_KEY = os.environ.get('COVALENT_API_KEY')
OPENSEA_API_KEY = os.environ.get('OPENSEA_API_KEY')

def set_api_keys(etherscan=None, bscscan=None, covalent=None, opensea=None):
    global ETHERSCAN_API_KEY, BSCSCAN_API_KEY, COVALENT_API_KEY, OPENSEA_API_KEY
    if etherscan:
        ETHERSCAN_API_KEY = etherscan
    if bscscan:
        BSCSCAN_API_KEY = bscscan
    if covalent:
        COVALENT_API_KEY = covalent
    if opensea:
        OPENSEA_API_KEY = opensea 