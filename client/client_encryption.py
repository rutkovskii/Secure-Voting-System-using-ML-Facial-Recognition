from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import hashlib
import json
import os
import time

def encrypt_data(data):
    with open('private_client_msg_key.pem', 'rb') as f:
        private_client_key = RSA.importKey(f.read())
    with open('public_server_msg_key.pem', 'rb') as f:
        public_server_key = RSA.importKey(f.read())
    keyLen = 32
    ivLen = AES.block_size
    #Convert data to string with json.dumps, then to bytes
    message = bytes(json.dumps(data), 'utf-8')

    #Create hash and digital signature
    hash = int.from_bytes(hashlib.sha512(message).digest(),byteorder='big')
    digital_signature_msg = pow(hash, private_client_key.d,private_client_key.n)

    #Create AES cipher and encrypt message
    key = get_random_bytes(keyLen)
    iv = get_random_bytes(ivLen)
    padded_plaintext = pad(message, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg_encryped = cipher.encrypt(padded_plaintext)

    #Encrypt AES key
    cipherAESkey = PKCS1_OAEP.new(public_server_key)
    Encrypted_AES_Key_msg = cipherAESkey.encrypt(key)

    #Return encrypted data
    return {
        'digital_signature': digital_signature_msg.to_bytes(2048,byteorder='big'),
        'msg_encrypted': msg_encryped,
        'encrypted_key': Encrypted_AES_Key_msg,
        'iv': iv
    }