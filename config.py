"""
Configuration file for the Bitcoin Wallet Key Checker.
Set your target address and API parameters here.
"""

# The target Bitcoin address to check against (set to your own address for safety).
USER_ADDRESS = ""  # e.g., "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

# Optional: Blockchain API settings
# Blockstream API base URL (no API key required for basic address info)
BLOCKSTREAM_API_URL = "https://blockstream.info/api"

# If using another service that requires an API key (e.g., Blockcypher), set here:
BLOCKCHAIN_API_KEY = ""
