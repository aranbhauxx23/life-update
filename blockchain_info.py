"""
Fetch public blockchain data for a given address using a REST API.
Example uses Blockstream or Blockchain.com endpoints.
"""

import requests
from config import BLOCKSTREAM_API_URL

def fetch_blockstream_address(address):
    """
    Fetch address info from Blockstream's API.
    Returns JSON with chain_stats and mempool_stats (if successful), or None on error.
    """
    url = f"{BLOCKSTREAM_API_URL}/address/{address}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data
    except Exception as e:
        print(f"Error fetching Blockstream data: {e}")
        return None

def fetch_blockchain_balance(address):
    """
    Fetch address balance from Blockchain.com's API.
    Returns JSON if successful, or None on error.
    """
    url = f"https://blockchain.info/rawaddr/{address}?format=json"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error fetching Blockchain.info data: {e}")
        return None
