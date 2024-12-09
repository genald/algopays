import base64, json
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def sha256_rsa_signed(payload: str, private_key: str):
    # Convert data to JSON string
    payload_data_str = json.dumps(payload, separators=(',', ':'))

    # Hash the data
    hashed_data = SHA256.new(payload_data_str.encode())

    # Load the private key
    private_key = RSA.import_key(private_key)

    # Sign the data
    signature = pkcs1_15.new(private_key).sign(hashed_data)
    
    # Encode the signature in Base64
    return base64.b64encode(signature).decode()
