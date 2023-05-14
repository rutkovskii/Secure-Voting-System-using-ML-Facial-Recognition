import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
import hashlib
from Crypto.PublicKey import RSA
import time
import shutil

message="34 Old Farm Lane"

key_pair = RSA.generate(2048)
public_client_msg_key = key_pair.publickey().export_key() # Kc+
private_client_msg_key = key_pair # Kc-

encrypt_folder = "/Users/braydenbergeron/PycharmProjects/547_Projects/encryption/"
decrypt_folder = "/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/"

public_client_msg_key_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/encryption/public_client_msg_key.pem'
public_server_msg_key_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/encryption/public_server_msg_key.pem'

with open(public_client_msg_key_path,'wb') as f:
	f.write(public_client_msg_key)

shutil.move(public_client_msg_key_path,decrypt_folder)
while not os.path.exists(public_server_msg_key_path):
	time.sleep(1)
with open(public_server_msg_key_path, 'rb') as f:
	public_server_msg_key = RSA.importKey(f.read())

mode = AES.MODE_CBC
keyLen = 32
ivLen = AES.block_size
message = bytes(message, 'utf-8')
hash = int.from_bytes(hashlib.sha512(message).digest(),byteorder='big')
digital_signature_msg = pow(hash, key_pair.d,key_pair.n)

with open('digital_signature_msg.bin','wb') as f:
	f.write(digital_signature_msg.to_bytes(2048,byteorder='big'))

digital_signature_msg_path = "/Users/braydenbergeron/PycharmProjects/547_Projects/encryption/digital_signature_msg.bin"
shutil.move(digital_signature_msg_path, decrypt_folder)

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

msg_encryped_path = os.path.join(encrypt_folder,'encryped_message.bin')
Encrypted_AES_Key_msg_path = os.path.join(encrypt_folder,'Encrypted_AES_Key_msg.bin')
iv_msg_path = os.path.join(encrypt_folder,'iv_msg.bin')

shutil.move(msg_encryped_path,decrypt_folder)
shutil.move(Encrypted_AES_Key_msg_path,decrypt_folder)
shutil.move(iv_msg_path,decrypt_folder)

os.remove(public_server_msg_key_path) # delete the public server key ks+