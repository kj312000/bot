import hashlib
import base58
import random
from ecdsa import SigningKey, SECP256k1
import requests
import time
import random  # Replace this with your actual logic

# Replace with your bot token and user ID
# Load environment variables from .env file
load_dotenv()

# Replace with your bot token and user ID from .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

start_value = 0x1c00000000000000000000000000000000
end_value = 0x1d00000000000000000000000000000000

# Function to convert private key to wallet address
def private_key_to_wallet_address(private_key, compressed=True):
    # Generate the public key using Elliptic Curve Cryptography (SECP256k1)
    sk = SigningKey.from_secret_exponent(private_key, curve=SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()  # Uncompressed public key

    # If compressed, adjust the public key format
    if compressed:
        public_key = (
            (b'\x02' if vk.pubkey.point.y() % 2 == 0 else b'\x03')
            + vk.pubkey.point.x().to_bytes(32, byteorder='big')
        )

    # Perform SHA-256 and RIPEMD-160 hashing
    public_key_hash = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160', public_key_hash).digest()

    # Add network prefix (0x00 for Bitcoin Mainnet)
    network_prefix = b'\x00'
    with_prefix = network_prefix + ripemd160

    # Compute checksum (double SHA256)
    checksum = hashlib.sha256(hashlib.sha256(with_prefix).digest()).digest()[:4]

    # Combine and encode in Base58
    final_address = base58.b58encode(with_prefix + checksum).decode()
    return final_address

def generate_keys_around_random():
    random_private_key = random.randint(start_value, end_value)

    key_range = 100000
    start_range = max(start_value, random_private_key - key_range)
    end_range = min(end_value, random_private_key + key_range)

    for private_key in range(start_range, end_range + 1):
        derived_wallet_address = private_key_to_wallet_address(private_key)
        if derived_wallet_address == "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so":
            print(f"Match found! Private Key: {hex(private_key)}, Wallet Address: {derived_wallet_address}")
            send_telegram_message(f"Match found! Private Key: {hex(private_key)}, Wallet Address: {derived_wallet_address}")
            return True

    return False

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

def main():
    match_found = False
    while not match_found:
        match_found = generate_keys_around_random()

    print("Finished checking keys.")

if __name__ == "__main__":
    main()
