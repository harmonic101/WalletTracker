class Web3ToolkitError(Exception):
    """Base exception for web3toolkit."""
    pass

class InvalidAddressError(Web3ToolkitError):
    """Raised when an invalid address is encountered."""
    pass

class TransactionError(Web3ToolkitError):
    """Raised for transaction-related errors."""
    pass

class ContractError(Web3ToolkitError):
    """Raised for contract-related errors."""
    pass

class TokenError(Web3ToolkitError):
    """Raised for token-related errors."""
    pass 