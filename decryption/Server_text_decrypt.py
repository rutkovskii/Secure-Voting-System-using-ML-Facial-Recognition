import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
from PIL import Image
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import hashlib



key_pair = RSA.generate(2048)
public_server_msg_key = key_pair.publickey().export_key()
private_server_msg_key = key_pair
with open('/Volumes/BB/ML_Encryption/public_server_msg_key.pem','wb') as f:
	f.write(public_server_msg_key)
while not os.path.exists('/Volumes/BB/ML_Encryption/public_client_msg_key.pem'):
    time.sleep(1)
with open('/Volumes/BB/ML_Encryption/public_client_msg_key.pem', 'rb') as f:
	public_client_key = RSA.importKey(f.read())

while not os.path.exists('/Volumes/BB/ML_Encryption/digital_signature_msg.bin'):
    time.sleep(1)
with open('/Volumes/BB/ML_Encryption/digital_signature_msg.bin', 'rb') as f:
	digital_signature_msg = int.from_bytes(f.read(),byteorder='big')
signature_hash_msg =  pow(digital_signature_msg,public_client_key.e,public_client_key.n)
mode = AES.MODE_CBC
keyLen = 32
ivLen = AES.block_size
with open("/Volumes/BB/ML_Encryption/Encrypted_AES_Key_msg.bin", 'rb') as f:
	AESKey=f.read()
cipherAES = PKCS1_OAEP.new(private_server_msg_key)
key = cipherAES.decrypt(AESKey)
with open("/Volumes/BB/ML_Encryption/iv_msg.bin", 'rb') as f:
	iv=f.read()
image_path = "/Volumes/BB/ML_Encryption/encryped_message.bin"
with open(image_path,'rb') as f:
	Encrypted_message = f.read()
# decrypt
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(Encrypted_message)
message_decrypted = unpad(plaintext, AES.block_size)

# integrity check
hashReceived = int.from_bytes(hashlib.sha512(message_decrypted).digest(),byteorder='big')
if signature_hash_msg==hashReceived:
	print("Verified")
else:
	print("Incorrect Hash")

print(message_decrypted.decode('utf-8'))

output_folder = "/Volumes/BB/ML_Encryption/message.txt"
with open(output_folder, 'wb') as f:
	f.write(message_decrypted)




