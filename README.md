# Bitcoin Wallet Key Checker

**Bitcoin Wallet Key Checker** is a Python tool (educational use only) that repeatedly generates random Bitcoin private keys and derives their corresponding addresses. It checks each address against a user-defined target address (`TARGET_ADDRESS` in `config.py`). All key attempts are logged, and if the target address is ever generated (extremely unlikely in practice), the matching private key is reported.

> **Warning:** Finding a Bitcoin private key by brute force is astronomically improbable due to the 2^256-size key space1718. This tool is intended solely for learning/demo purposes19. Do **not** use it on real wallets or others’ addresses.

## Setup

1. **Clone the repository** and navigate into it.
2. **Edit `config.py`**: set `TARGET_ADDRESS` to the Bitcoin address you want to check (your own address, for testing).  
3. **Install dependencies** using pip:

   ```bash
   pip install -r requirements.txt
