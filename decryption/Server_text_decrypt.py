import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
from PIL import Image
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import hashlib
import shutil

key_pair = RSA.generate(2048)
public_server_msg_key = key_pair.publickey().export_key()
private_server_msg_key = key_pair

encrypt_folder = "/Users/braydenbergeron/PycharmProjects/547_Projects/encryption/"
decrypt_folder = "/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/"

public_server_msg_key_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/public_server_msg_key.pem'
public_client_msg_key_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/public_client_msg_key.pem'

with open(public_server_msg_key_path,'wb') as f:
	f.write(public_server_msg_key)
shutil.move(public_server_msg_key_path,encrypt_folder)

while not os.path.exists(public_client_msg_key_path):
	time.sleep(1)
with open(public_client_msg_key_path, 'rb') as f:
	public_client_key = RSA.importKey(f.read())

digital_signature_msg_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/digital_signature_msg.bin'
while not os.path.exists(digital_signature_msg_path):
	time.sleep(1)
with open(digital_signature_msg_path, 'rb') as f:
	digital_signature_msg = int.from_bytes(f.read(),byteorder='big')
signature_hash_msg =  pow(digital_signature_msg,public_client_key.e,public_client_key.n)
mode = AES.MODE_CBC
keyLen = 32
ivLen = AES.block_size

Encrypted_AES_Key_msg_Path = '/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/Encrypted_AES_Key_msg.bin'
iv_msg_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/iv_msg.bin'
file_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/encryped_message.bin'

with open(Encrypted_AES_Key_msg_Path, 'rb') as f:
	AESKey=f.read()
cipherAES = PKCS1_OAEP.new(private_server_msg_key)
key = cipherAES.decrypt(AESKey)

with open(iv_msg_path, 'rb') as f:
	iv=f.read()
with open(file_path,'rb') as f:
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

output_path = os.path.join(decrypt_folder,"voter_message.txt")
with open(output_path, 'wb') as f:
	f.write(message_decrypted)

if (input("Remove[Y/N]")=="Y"):
	os.remove(iv_msg_path) # delete the AES IV
	os.remove(Encrypted_AES_Key_msg_Path) # delete the encrypted AES key ks+(kAES)
	os.remove(public_client_msg_key_path) # delete the public client key Kc+
	os.remove(file_path) # delete the encrypted image
	os.remove(digital_signature_msg_path) # delete the digital signature
	os.remove(output_path) # delete the decrypted image




