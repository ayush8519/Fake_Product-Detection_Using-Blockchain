# Fake Product Identification Using Blockchain

## Project Overview
This application uses **Ethereum Blockchain** + **Digital Signatures** to authenticate product barcodes and detect counterfeit products. Barcode images are converted to SHA-256 hashes stored on-chain; any fake/cloned barcode produces a mismatched signature.

---

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | HTML, Bootstrap 5, Jinja2 |
| Backend | Python Flask |
| Blockchain | Ethereum (Ganache local chain) |
| Smart Contract | Solidity 0.5.x |
| Python ↔ Ethereum | Web3.py |
| Image Hashing | PIL + SHA-256 |

---

## Setup Instructions

### Step 1 – Install Node.js Dependencies (for Ethereum)
```bash
npm install -g ganache-cli truffle
```

### Step 2 – Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 – Start Local Blockchain (Ganache)
Open a terminal and run:
```bash
ganache-cli --port 7545 --networkId 5777
```
Or double-click `hello-eth/runBlockchain.bat`

### Step 4 – Deploy Smart Contract
```bash
cd hello-eth
truffle migrate --reset
```
Copy the **FakeProduct contract address** printed in the output.

### Step 5 – Configure Contract Address
Open `blockchain.py` and replace:
```python
CONTRACT_ADDRESS = "0xYourDeployedContractAddressHere"
```
with the actual deployed address from Step 4.

### Step 6 – Start Flask Server
```bash
python app.py
```
Or double-click `run.bat`

### Step 7 – Open Browser
```
http://127.0.0.1:5000/index
```

---

## Modules

### Admin (username: admin, password: admin)
- **Add Product Details** – Enter product info + upload barcode image → system generates SHA-256 digital signature → stores all data on Blockchain
- **View Product Details** – View all products stored on Blockchain
- **View User Details** – View all registered users on Blockchain

### User
- **User Signup** – Register; credentials stored on Blockchain
- **User Login** – Authenticate using Blockchain
- **Retrieve Product Data** – Fetch product details by ID from Blockchain
- **Authenticate Scan** – Upload a barcode image → system generates signature → compares with Blockchain → AUTHENTIC or FAKE

---

## How Authentication Works
1. Admin uploads barcode image → SHA-256 hash generated → stored on Ethereum Blockchain
2. User uploads same/different barcode → SHA-256 hash generated
3. If hashes match → **AUTHENTIC** ✅
4. If hashes differ → **FAKE DETECTED** ❌

Blockchain ensures the stored signature cannot be altered (tamper-proof).
