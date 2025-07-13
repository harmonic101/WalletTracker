# Wallet Tracker - Stolen Funds Monitor

This project is a tool developed to track stolen funds from wallet addresses using the web3toolkit library.

## 🚀 Features

- **Real-time Monitoring**: Continuously tracks wallet activities
- **Suspicious Activity Analysis**: Detects large transfers and suspicious transactions
- **Multi-Blockchain Support**: Supports Ethereum, Bitcoin and other networks
- **Report Generation**: Creates detailed analysis reports
- **Alert System**: Provides instant alerts for suspicious transactions

## 📋 Requirements

```bash
pip install requests
```

The web3toolkit library must be present in the project folder.

## 🛠️ Installation

1. Clone the project:
```bash
cd example_project
```

2. Install required libraries:
```bash
pip install requests
```

3. Make sure web3toolkit is in the main directory.

## 🎯 Usage

### Basic Usage

```python
from wallet_tracker import WalletTracker

# Initialize wallet tracker
tracker = WalletTracker("0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6", "ethereum")

# Get current balance
balance = tracker.get_wallet_balance()
print(f"Balance: {balance}")

# Get transaction history
transactions = tracker.get_transaction_history(limit=50)
print(f"Total transactions: {len(transactions)}")

# Analyze suspicious activities
suspicious = tracker.analyze_suspicious_activity(transactions)
for sus in suspicious:
    print(f"Suspicious: {sus['reason']}")

# Generate report
report = tracker.generate_report("report.txt")
```

### Real-time Monitoring

```python
# Start continuous monitoring (check every 30 seconds)
tracker.start_monitoring(interval=30)
```

### Running from Command Line

```bash
python wallet_tracker.py
```

The program will ask you for a wallet address and automatically:
1. Show current balance
2. Analyze transaction history
3. Detect suspicious activities
4. Generate detailed report
5. Offer real-time monitoring option

## 🔍 Suspicious Activity Detection

The program marks the following situations as suspicious:

- **Large Transfers**: Transfers over 1 ETH
- **Rapid Sequential Transfers**: Multiple transfers made in a short time
- **Transfers to Unknown Addresses**: Transfers to addresses not seen before

## 📊 Report Format

Generated reports contain the following information:

```
WALLET TRACKER REPORT
====================
Target Address: 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
Network: ethereum
Generated: 2024-01-15 14:30:25

CURRENT BALANCE:
{
  "ETH": 0.5,
  "USDT": 1000.0
}

TRANSACTION SUMMARY:
Total Transactions: 15
Suspicious Transactions: 3

SUSPICIOUS ACTIVITY:
1. Large transfer detected: 5.2500 ETH
   Risk Level: MEDIUM
   Transaction Hash: 0x1234...
   To Address: 0x5678...
   Value: 5.2500 ETH
```

## ⚠️ Warnings

- This tool is for educational and development purposes only
- Use professional tools for real money tracking
- Pay attention to API limits
- Protect personal data

## 🐛 Troubleshooting

### web3toolkit Import Error
```
Error: web3toolkit not found. Please install it first.
```
**Solution**: Make sure the web3toolkit folder is in the main directory.

### Network Connection Error
```
❌ Failed to connect to ethereum: Connection error
```
**Solution**: Check your internet connection and ensure API endpoints are working.

### Cannot Get Transaction History
```
❌ Error getting transaction history: API limit exceeded
```
**Solution**: Check API limits and make requests with longer intervals.

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Contact

You can open an issue for questions or send a pull request. 