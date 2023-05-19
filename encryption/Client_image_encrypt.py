import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
from PIL import Image
import hashlib
from Crypto.PublicKey import RSA
import time

import shutil

key_pair = RSA.generate(2048)
public_client_key = key_pair.publickey().export_key() # Kc+
private_client_key = key_pair # Kc-

encrypt_folder = "/Users/braydenbergeron/PycharmProjects/547_Projects/encryption/"
decrypt_folder = "/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/"

public_client_key_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/encryption/public_client_key.pem'
public_server_key_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/encryption/public_server_key.pem'

with open(public_client_key_path,'wb') as f:
	f.write(public_client_key)
shutil.move(public_client_key_path,decrypt_folder)
while not os.path.exists(public_server_key_path):
    time.sleep(1)
with open(public_server_key_path, 'rb') as f:
	public_server_key = RSA.importKey(f.read())


mode = AES.MODE_CBC # AES in CBC (Cipher Block Chaining) to encrypt
keyLen = 32 # AES 256 has 32 byte key
ivLen = AES.block_size # set IV equal to block length
file_path = "/Users/braydenbergeron/Desktop/ECE_547/ML_Encryption/Original_Images/Joe_Biden/Joe_Biden6.jpg"

with open(file_path, "rb") as f: # read image jpeg
	face_original = f.read()
facehash = Image.open(file_path) # open image file again for hashing from bytes
hash = int.from_bytes(hashlib.sha512(facehash.tobytes()).digest(),byteorder='big')
digital_signature = pow(hash, key_pair.d,key_pair.n) # digital signature using private client key to sign

with open('digital_signature.bin','wb') as f: # write the digital signature as a .bin
	f.write(digital_signature.to_bytes(2048,byteorder='big'))

digital_signature_path = "/Users/braydenbergeron/PycharmProjects/547_Projects/encryption/digital_signature.bin"
shutil.move(digital_signature_path,decrypt_folder) # replace with HTTP TLS transport mechanism to server

key = get_random_bytes(keyLen) # generate random key
iv = get_random_bytes(ivLen) # generate random IV

padded_plaintext = pad(face_original, AES.block_size)
cipher = AES.new(key, AES.MODE_CBC, iv) # create the AES cipher key

face_encrypted = cipher.encrypt(padded_plaintext) # encrypt the image with the AES key

output_path = os.path.join(encrypt_folder, f"voter_image.enc")

cipherAESkey = PKCS1_OAEP.new(public_server_key)
Encrypted_AES_Key = cipherAESkey.encrypt(key)
with open('Encrypted_AES_Key.bin','wb') as f:
	f.write(Encrypted_AES_Key)
with open('iv.bin', 'wb') as f:
	f.write(iv)
with open(output_path,'wb') as f:
	f.write(face_encrypted)

Encrypted_AES_Key_path = os.path.join(encrypt_folder,'Encrypted_AES_Key.bin')
iv_path = os.path.join(encrypt_folder,'iv.bin')

shutil.move(output_path,decrypt_folder)
shutil.move(Encrypted_AES_Key_path,decrypt_folder)
shutil.move(iv_path,decrypt_folder)

os.remove(public_server_key_path) # delete the public server key ks+
