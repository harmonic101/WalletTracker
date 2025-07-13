"""
Wallet Tracker - Stolen Funds Monitor
====================================

This project demonstrates how to track stolen funds from a wallet address
using the web3toolkit library. It monitors transactions and alerts when
funds are moved from the target wallet.

Features:
- Real-time transaction monitoring
- Multiple blockchain support (Ethereum, Bitcoin)
- Transaction history analysis
- Alert system for suspicious activities
- Export functionality for reports

Author: Web3 Development Team
Version: 1.0.0
"""

import time
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import sys
import os

# Add web3toolkit to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from web3toolkit import wallet, network, transaction
    print("✅ web3toolkit imported successfully")
except ImportError as e:
    print(f"❌ Error importing web3toolkit: {e}")
    print(f"Current path: {sys.path}")
    sys.exit(1)


class WalletTracker:
    def __init__(self, target_address: str, network_name: str = "ethereum"):
        """
        Initialize wallet tracker for monitoring stolen funds.
        
        Args:
            target_address: The wallet address to monitor
            network_name: Blockchain network (ethereum, bitcoin, etc.)
        """
        self.target_address = target_address.lower()
        self.network_name = network_name
        self.transaction_history = []
        self.suspicious_transactions = []
        self.last_checked_block = 0
        
        # Initialize network connection
        try:
            self.network = network.Network(network_name)
            print(f"✅ Connected to {network_name} network")
        except Exception as e:
            print(f"❌ Failed to connect to {network_name}: {e}")
            sys.exit(1)
    
    def get_wallet_balance(self) -> Dict[str, float]:
        """
        Get current wallet balance.
        
        Returns:
            Dictionary with token balances
        """
        try:
            wallet_info = wallet.Wallet(self.target_address, self.network)
            return wallet_info.get_balance()
        except Exception as e:
            print(f"❌ Error getting balance: {e}")
            return {}
    
    def get_transaction_history(self, limit: int = 100) -> List[Dict]:
        """
        Get recent transaction history.
        
        Args:
            limit: Number of transactions to fetch
            
        Returns:
            List of transaction dictionaries
        """
        try:
            wallet_info = wallet.Wallet(self.target_address, self.network)
            transactions = wallet_info.get_transactions(limit=limit)
            
            # Filter for outgoing transactions (potential theft)
            outgoing_txs = []
            for tx in transactions:
                if tx.get('from', '').lower() == self.target_address:
                    outgoing_txs.append({
                        'hash': tx.get('hash'),
                        'to': tx.get('to'),
                        'value': tx.get('value'),
                        'timestamp': tx.get('timestamp'),
                        'gas_used': tx.get('gas_used'),
                        'status': tx.get('status')
                    })
            
            return outgoing_txs
        except Exception as e:
            print(f"❌ Error getting transaction history: {e}")
            return []
    
    def analyze_suspicious_activity(self, transactions: List[Dict]) -> List[Dict]:
        """
        Analyze transactions for suspicious patterns.
        
        Args:
            transactions: List of transactions to analyze
            
        Returns:
            List of suspicious transactions
        """
        suspicious = []
        
        for tx in transactions:
            # Check for large transfers (potential theft)
            value_eth = float(tx.get('value', 0)) / 1e18  # Convert from wei to ETH
            
            if value_eth > 1.0:  # Flag transfers over 1 ETH
                suspicious.append({
                    'transaction': tx,
                    'reason': f'Large transfer detected: {value_eth:.4f} ETH',
                    'risk_level': 'HIGH' if value_eth > 10 else 'MEDIUM'
                })
            
            # Check for multiple rapid transfers
            # (This would need more sophisticated analysis in a real implementation)
        
        return suspicious
    
    def track_new_transactions(self) -> List[Dict]:
        """
        Monitor for new transactions in real-time.
        
        Returns:
            List of new transactions
        """
        try:
            current_block = self.network.get_latest_block_number()
            
            if current_block > self.last_checked_block:
                # Get new transactions
                new_transactions = self.get_transaction_history(limit=10)
                
                # Filter for transactions we haven't seen before
                new_txs = []
                for tx in new_transactions:
                    if tx not in self.transaction_history:
                        new_txs.append(tx)
                        self.transaction_history.append(tx)
                
                self.last_checked_block = current_block
                return new_txs
            
            return []
        except Exception as e:
            print(f"❌ Error tracking new transactions: {e}")
            return []
    
    def generate_report(self, filename: str = None) -> str:
        """
        Generate a comprehensive report of wallet activity.
        
        Args:
            filename: Optional filename to save report
            
        Returns:
            Report content as string
        """
        balance = self.get_wallet_balance()
        transactions = self.get_transaction_history()
        suspicious = self.analyze_suspicious_activity(transactions)
        
        report = f"""
WALLET TRACKER REPORT
====================
Target Address: {self.target_address}
Network: {self.network_name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CURRENT BALANCE:
{json.dumps(balance, indent=2)}

TRANSACTION SUMMARY:
Total Transactions: {len(transactions)}
Suspicious Transactions: {len(suspicious)}

SUSPICIOUS ACTIVITY:
"""
        
        for i, sus in enumerate(suspicious, 1):
            report += f"""
{i}. {sus['reason']}
   Risk Level: {sus['risk_level']}
   Transaction Hash: {sus['transaction']['hash']}
   To Address: {sus['transaction']['to']}
   Value: {float(sus['transaction']['value']) / 1e18:.4f} ETH
"""
        
        if filename:
            with open(filename, 'w') as f:
                f.write(report)
            print(f"📄 Report saved to {filename}")
        
        return report
    
    def start_monitoring(self, interval: int = 30):
        """
        Start real-time monitoring of the wallet.
        
        Args:
            interval: Check interval in seconds
        """
        print(f"🔍 Starting monitoring for {self.target_address}")
        print(f"⏱️  Check interval: {interval} seconds")
        print("Press Ctrl+C to stop monitoring\n")
        
        try:
            while True:
                new_transactions = self.track_new_transactions()
                
                if new_transactions:
                    print(f"🚨 {len(new_transactions)} new transaction(s) detected!")
                    
                    for tx in new_transactions:
                        value_eth = float(tx.get('value', 0)) / 1e18
                        print(f"   📤 Outgoing: {value_eth:.4f} ETH to {tx.get('to')}")
                        
                        if value_eth > 1.0:
                            print(f"   ⚠️  WARNING: Large transfer detected!")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
            self.generate_report(f"wallet_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")


def main():
    """Main function to demonstrate wallet tracking."""
    print("🔍 Wallet Tracker - Stolen Funds Monitor")
    print("=" * 50)
    
    # Example wallet address (replace with actual address to monitor)
    target_address = input("Enter wallet address to monitor: ").strip()
    
    if not target_address:
        print("❌ No address provided. Using example address.")
        target_address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"  # Example address
    
    # Initialize tracker
    tracker = WalletTracker(target_address, "ethereum")
    
    # Show current balance
    balance = tracker.get_wallet_balance()
    print(f"\n💰 Current Balance: {json.dumps(balance, indent=2)}")
    
    # Get transaction history
    print("\n📊 Fetching transaction history...")
    transactions = tracker.get_transaction_history(limit=20)
    print(f"📈 Found {len(transactions)} outgoing transactions")
    
    # Analyze for suspicious activity
    suspicious = tracker.analyze_suspicious_activity(transactions)
    if suspicious:
        print(f"⚠️  Found {len(suspicious)} suspicious transactions!")
        for sus in suspicious:
            print(f"   - {sus['reason']}")
    
    # Generate report
    print("\n📄 Generating report...")
    report = tracker.generate_report()
    print(report)
    
    # Ask if user wants to start monitoring
    monitor = input("\n🔍 Start real-time monitoring? (y/n): ").lower().strip()
    if monitor == 'y':
        tracker.start_monitoring()
    else:
        print("👋 Goodbye!")


if __name__ == "__main__":
    main() 