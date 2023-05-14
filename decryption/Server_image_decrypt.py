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
public_server_key = key_pair.publickey().export_key()
private_server_key = key_pair

encrypt_folder = "/Users/braydenbergeron/PycharmProjects/547_Projects/encryption/"
decrypt_folder = "/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/"

public_server_key_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/public_server_key.pem'
public_client_key_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/public_client_key.pem'

with open(public_server_key_path,'wb') as f:
	f.write(public_server_key)
shutil.move(public_server_key_path,encrypt_folder)

while not os.path.exists(public_client_key_path):
	time.sleep(1)
with open(public_client_key_path, 'rb') as f:
	public_client_key = RSA.importKey(f.read())

digital_signature_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/digital_signature.bin'
while not os.path.exists(digital_signature_path):
	time.sleep(1)
with open(digital_signature_path, 'rb') as f:
	digital_signature = int.from_bytes(f.read(),byteorder='big')
signature_hash =  pow(digital_signature,public_client_key.e,public_client_key.n)


mode = AES.MODE_CBC
keyLen = 32
ivLen = AES.block_size
Encrypted_AES_Key_Path = '/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/Encrypted_AES_Key.bin'
iv_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/iv.bin'
image_path = '/Users/braydenbergeron/PycharmProjects/547_Projects/decryption/voter_image.enc'

with open(Encrypted_AES_Key_Path, 'rb') as f:
	AESKey=f.read()
cipherAES = PKCS1_OAEP.new(private_server_key)
key = cipherAES.decrypt(AESKey)

with open(iv_path, 'rb') as f:
	iv=f.read()

with open(image_path,'rb') as f:
	Encrypted_Face = f.read()

# decrypt
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(Encrypted_Face)
Face_decrypted = unpad(plaintext, AES.block_size)

# integrity check

output_path = os.path.join(decrypt_folder,"voter_image.jpg")
with open(output_path, 'wb') as f:
	f.write(Face_decrypted)

facehash = Image.open(output_path)
hashReceived = int.from_bytes(hashlib.sha512(facehash.tobytes()).digest(),byteorder='big')
if signature_hash==hashReceived:
	print("Verified")
else:
	print("Incorrect Hash")

if (input("Remove[Y/N]")=="Y"):
	os.remove(iv_path) # delete the AES IV
	os.remove(Encrypted_AES_Key_Path) # delete the encrypted AES key ks+(kAES)
	os.remove(public_client_key_path) # delete the public client key Kc+
	os.remove(image_path) # delete the encrypted image
	os.remove(digital_signature_path) # delete the digital signature
	os.remove(output_path) # delete the decrypted image

