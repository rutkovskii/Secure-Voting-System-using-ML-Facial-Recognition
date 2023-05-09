import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
import hashlib
from Crypto.PublicKey import RSA
import time

key_pair = RSA.generate(2048)
public_client_msg_key = key_pair.publickey().export_key()
private_client_msg_key = key_pair
with open('/Volumes/BB/ML_Encryption/public_client_msg_key.pem','wb') as f:
	f.write(public_client_msg_key)
while not os.path.exists('public_server_msg_key.pem'):
    time.sleep(1)
with open('/Volumes/BB/ML_Encryption/public_server_msg_key.pem', 'rb') as f:
	public_server_msg_key = RSA.importKey(f.read())

mode = AES.MODE_CBC
keyLen = 32
ivLen = AES.block_size
message="34 Old Farm Lane"
message = bytes(message, 'utf-8')
hash = int.from_bytes(hashlib.sha512(message).digest(),byteorder='big')
digital_signature_msg = pow(hash, key_pair.d,key_pair.n)

with open('digital_signature_msg.bin','wb') as f:
	f.write(digital_signature_msg.to_bytes(2048,byteorder='big'))

key = get_random_bytes(keyLen)
iv = get_random_bytes(ivLen)

padded_plaintext = pad(message, AES.block_size)
cipher = AES.new(key, AES.MODE_CBC, iv)

msg_encryped = cipher.encrypt(padded_plaintext)

cipherAESkey = PKCS1_OAEP.new(public_server_msg_key)
Encrypted_AES_Key_msg = cipherAESkey.encrypt(key)
with open('Encrypted_AES_Key_msg.bin','wb') as f:
	f.write(Encrypted_AES_Key_msg)
with open('iv_msg.bin', 'wb') as f:
	f.write(iv)
with open('encryped_message.bin','wb') as f:
	f.write(msg_encryped)

