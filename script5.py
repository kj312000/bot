import hashlib
import base58
import random
from ecdsa import SigningKey, SECP256k1
import requests
import time
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Telegram bot settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Set up logging for this script
logging.basicConfig(level=logging.INFO)

start_value = 0x1e00000000000000000000000000000000
end_value = 0x1f00000000000000000000000000000000

# Function to convert private key to wallet address
def private_key_to_wallet_address(private_key, compressed=True):
    sk = SigningKey.from_secret_exponent(private_key, curve=SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()  # Uncompressed public key

    if compressed:
        public_key = (
            (b'\x02' if vk.pubkey.point.y() % 2 == 0 else b'\x03')
            + vk.pubkey.point.x().to_bytes(32, byteorder='big')
        )

    public_key_hash = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160', public_key_hash).digest()

    network_prefix = b'\x00'
    with_prefix = network_prefix + ripemd160

    checksum = hashlib.sha256(hashlib.sha256(with_prefix).digest()).digest()[:4]

    final_address = base58.b58encode(with_prefix + checksum).decode()
    return final_address

# Function to generate keys and check for a match
def generate_keys_around_random():
    random_private_key = random.randint(start_value, end_value)
    print(hex(random_private_key)[2:])
    key_range = 100000
    start_range = max(start_value, random_private_key - key_range)
    end_range = min(end_value, random_private_key + key_range)

    for private_key in range(start_range, end_range + 1):
        derived_wallet_address = private_key_to_wallet_address(private_key)
        if derived_wallet_address == "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so":
            logging.info(f"Match found! Private Key: {hex(private_key)}, Wallet Address: {derived_wallet_address}")
            send_telegram_message(f"Match found! Private Key: {hex(private_key)}, Wallet Address: {derived_wallet_address}")
            return True

    return False

# Function to send Telegram message
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

# Main function to keep checking until a match is found
def main():
    logging.info("Script started.")
    match_found = False
    while not match_found:
        match_found = generate_keys_around_random()

    logging.info("Finished checking keys.")

if __name__ == "__main__":
    main()
