import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
from PIL import Image
import hashlib
from Crypto.PublicKey import RSA
import time

key_pair = RSA.generate(2048)
public_client_key = key_pair.publickey().export_key()
private_client_key = key_pair
with open('/Volumes/BB/ML_Encryption/public_client_key.pem','wb') as f:
	f.write(public_client_key)
while not os.path.exists('public_server_key.pem'):
    time.sleep(1)
with open('/Volumes/BB/ML_Encryption/public_server_msg_key.pem', 'rb') as f:
	public_server_key = RSA.importKey(f.read())

encrypt_folder = "Encrypted_AES_Images\\"
original_folder = "Original_Images\\"
mode = AES.MODE_CBC

i=1
keyLen = 32
ivLen = AES.block_size
file_path = "/Volumes/BB/ML_Encryption/Encrypted_Images/Brayden/Brayden1_0_.jpg"
with open(file_path, "rb") as f:
        face_original = f.read()
facehash = Image.open(file_path)
hash = int.from_bytes(hashlib.sha512(facehash.tobytes()).digest(),byteorder='big')
#hash_bytes = bytes.fromhex(hash)
digital_signature = pow(hash, key_pair.d,key_pair.n)

with open('digital_signature.bin','wb') as f:
	f.write(digital_signature.to_bytes(2048,byteorder='big'))

key = get_random_bytes(keyLen)
iv = get_random_bytes(ivLen)

padded_plaintext = pad(face_original, AES.block_size)
cipher = AES.new(key, AES.MODE_CBC, iv)

face_encrypted = cipher.encrypt(padded_plaintext)

#paddedSize = len(padded_plaintext) - len(face_original)
#void = columnOrig * depthOrig - ivLen - paddedSize
#ivCiphertextVoid = iv + face_encrypted + bytes(void)
#imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype=orig.dtype).reshape(rowOrig+1,columnOrig,depthOrig)

output_folder = os.path.join(encrypt_folder)
if not os.path.exists(output_folder):
	os.makedirs(output_folder)
output_path = os.path.join(output_folder, f"Brayden1.enc")

cipherAESkey = PKCS1_OAEP.new(public_server_key)
Encrypted_AES_Key = cipherAESkey.encrypt(key)
with open('Encrypted_AES_Key.bin','wb') as f:
	f.write(Encrypted_AES_Key)
with open('iv.bin', 'wb') as f:
	f.write(iv)
with open(output_path,'wb') as f:
	f.write(face_encrypted)
i+=1