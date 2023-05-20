import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import time
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import hashlib
import json


def decrypt_data(data):
    with open("private_server_msg_key.pem", "rb") as f:
        private_server_key = RSA.importKey(f.read())
    with open("public_client_msg_key.pem", "rb") as f:
        public_client_key = RSA.importKey(f.read())

    # Convert data to string with json.dumps, then to bytes
    message = bytes(json.dumps(data), "utf-8")

    # receive digital signature and apply public client key
    while not os.path.exists("/Volumes/BB/ML_Encryption/digital_signature_msg.bin"):
        time.sleep(1)
    with open("/Volumes/BB/ML_Encryption/digital_signature_msg.bin", "rb") as f:
        digital_signature_msg = int.from_bytes(f.read(), byteorder="big")
    signature_hash_msg = pow(
        digital_signature_msg, public_client_key.e, public_client_key.n
    )

    # decrypt AES key
    mode = AES.MODE_CBC
    keyLen = 32
    ivLen = AES.block_size
    with open("/Volumes/BB/ML_Encryption/Encrypted_AES_Key_msg.bin", "rb") as f:
        AESKey = f.read()
    cipherAES = PKCS1_OAEP.new(private_server_key)
    key = cipherAES.decrypt(AESKey)
    with open("/Volumes/BB/ML_Encryption/iv_msg.bin", "rb") as f:
        iv = f.read()

    msg_encrypted_path = "/Volumes/BB/ML_Encryption/msg_encrypted.bin"
    with open(msg_encrypted_path, "rb") as f:
        Encrypted_message = f.read()

    # decrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(Encrypted_message)
    message_decrypted = unpad(plaintext, AES.block_size)

    # integrity check
    hashReceived = int.from_bytes(
        hashlib.sha512(message_decrypted).digest(), byteorder="big"
    )
    if signature_hash_msg == hashReceived:
        verified = 1
    else:
        verified = 0

    return {"verified": verified, "msg_decrypted": message_decrypted}

    """print(message_decrypted.decode('utf-8'))
    
    output_folder = "/Volumes/BB/ML_Encryption/message.txt"
    with open(output_folder, 'wb') as f:
        f.write(message_decrypted)"""
