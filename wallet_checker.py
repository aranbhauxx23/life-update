"""
Main script for the Bitcoin Wallet Key Checker.
Continuously generates random private keys, derives their addresses, and compares to the target.
Logs each attempt and stops if the target address is found.
"""

import sys
import threading
import secrets
import hashlib
from ecdsa import SECP256k1, SigningKey
from logger import setup_logger
from config import USER_ADDRESS
from blockchain_info import fetch_blockstream_address, fetch_blockchain_balance

# Setup logging
logger = setup_logger()

# Global stop event for threads
stop_event = threading.Event()

def private_key_to_address(priv_key_hex):
    """
    Given a private key in hex (64 chars), derive the compressed public key and P2PKH address.
    Follows Bitcoin's address generation (double SHA-256 + RIPEMD-160 + Base58Check).
    """
    # Convert hex to SigningKey (ECDSA)
    priv_key_bytes = bytes.fromhex(priv_key_hex)
    sk = SigningKey.from_string(priv_key_bytes, curve=SECP256k1)
    vk = sk.get_verifying_key()

    # Compressed public key: 02 or 03 prefix + X coordinate
    x = vk.to_string()[:32]
    y = vk.to_string()[32:]
    prefix = b'\x02' if (y[-1] % 2 == 0) else b'\x03'
    pub_key_compressed = prefix + x

    # SHA-256 and then RIPEMD-160
    sha256_hash = hashlib.sha256(pub_key_compressed).digest()
    ripemd160 = hashlib.new('ripemd160', sha256_hash).digest()

    # Mainnet version byte 0x00 + RIPEMD-160 hash, then double SHA-256 checksum
    versioned_payload = b'\x00' + ripemd160
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
    address_bytes = versioned_payload + checksum

    # Base58 encoding
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    num = int.from_bytes(address_bytes, 'big')
    result = ''
    while num > 0:
        num, rem = divmod(num, 58)
        result = alphabet[rem] + result
    # Handle leading zeros (1's)
    n_pad = len(address_bytes) - len(address_bytes.lstrip(b'\x00'))
    return '1' * n_pad + result

def key_generation_thread(target_address):
    """
    Thread worker: continuously generate keys and compare addresses.
    Stops if a match is found (signalled by stop_event).
    """
    while not stop_event.is_set():
        # Generate a random 256-bit integer < curve order
        priv_int = secrets.randbelow(SECP256k1.order)
        if priv_int == 0:
            continue  # Very unlikely; avoid the zero key
        priv_hex = f"{priv_int:064x}"
        addr = private_key_to_address(priv_hex)

        logger.info(f"Attempt: Address={addr} | PrivKey={priv_hex}")
        # Compare (case-insensitive for addresses)
        if addr == target_address:
            logger.info(f"*** MATCH FOUND! Address {addr} corresponds to private key {priv_hex} ***")
            print(f"*** MATCH FOUND! Private key (hex): {priv_hex} ***")
            stop_event.set()
            break

def main():
    # Determine target address
    address = USER_ADDRESS.strip()
    if not address:
        address = input("Enter your Bitcoin address: ").strip()
    print(f"Target address: {address}")

    # Fetch blockchain info for context (optional)
    try:
        info = fetch_blockchain_balance(address)
        if info and 'final_balance' in info:
            bal = info.get('final_balance', 0)
            print(f"Balance (Satoshi): {bal}, Transactions: {info.get('n_tx',0)}")
    except Exception:
        pass

    # Start multiple worker threads
    num_threads = 4  # adjust as needed
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=key_generation_thread, args=(address,), name=f"Worker-{i+1}")
        t.start()
        threads.append(t)

    try:
        # Wait for threads to finish (they won't unless stopped)
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("Interrupted by user. Stopping threads...")
        stop_event.set()
        for t in threads:
            t.join()

if __name__ == "__main__":
    main()
