from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import hashlib
import json
import os

from config import Config


def encrypt_data(data):
    with open(
        os.path.join(Config.SECURITY_DIR, "private_client_msg_key.pem"), "rb"
    ) as f:
        private_key = RSA.importKey(f.read())
    with open(
        os.path.join(Config.SECURITY_DIR, "public_server_msg_key.pem"), "rb"
    ) as f:
        public_key = RSA.importKey(f.read())

    keyLen = 32
    ivLen = AES.block_size
    # Convert data to string with json.dumps, then to bytes
    message = bytes(json.dumps(data), "utf-8")

    # Create hash and digital signature
    hash = int.from_bytes(hashlib.sha512(message).digest(), byteorder="big")

    digital_signature_msg = pow(hash, private_key.d, private_key.n)

    # Create AES cipher and encrypt message
    key = get_random_bytes(keyLen)
    iv = get_random_bytes(ivLen)
    padded_plaintext = pad(message, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg_encryped = cipher.encrypt(padded_plaintext)

    # Encrypt AES key
    cipherAESkey = PKCS1_OAEP.new(public_key)
    Encrypted_AES_Key_msg = cipherAESkey.encrypt(key)

    # Return encrypted data
    return {
        "digital_signature": digital_signature_msg,
        "msg_encrypted": int.from_bytes(msg_encryped, byteorder="big"),
        "encrypted_key": int.from_bytes(Encrypted_AES_Key_msg, byteorder="big"),
        "iv": int.from_bytes(iv, byteorder="big"),
    }


"""with open('example_request.json') as user_file:
  f = user_file.read()
x=encrypt_data(f)
with open('json_test.json', "w") as file:
    json.dump(x, file)"""
