import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
from PIL import Image
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import hashlib

key_pair = RSA.generate(2048)
public_server_key = key_pair.publickey().export_key()
private_server_key = key_pair
with open('C:\\Users\\Brayd\\Documents\\UMass\\ECE_547\\ML_Encryption\\public_server_key.pem','wb') as f:
	f.write(public_server_key)
while not os.path.exists('C:\\Users\\Brayd\\Documents\\UMass\\ECE_547\\ML_Encryption\\public_client_key.pem'):
    time.sleep(1)
with open('C:\\Users\\Brayd\\Documents\\UMass\\ECE_547\\ML_Encryption\\public_client_key.pem', 'rb') as f:
	public_client_key = RSA.importKey(f.read())

while not os.path.exists('C:\\Users\\Brayd\\Documents\\UMass\\ECE_547\\ML_Encryption\\digital_signature.bin'):
    time.sleep(1)
with open('C:\\Users\\Brayd\\Documents\\UMass\\ECE_547\\ML_Encryption\\digital_signature.bin', 'rb') as f:
	digital_signature = int.from_bytes(f.read(),byteorder='big')
signature_hash =  pow(digital_signature,public_client_key.e,public_client_key.n)
mode = AES.MODE_CBC
keyLen = 32
ivLen = AES.block_size
with open("C:\\Users\\Brayd\\Documents\\UMass\\ECE_547\\ML_Encryption\\Encrypted_AES_Key.bin", 'rb') as f:
	AESKey=f.read()
cipherAES = PKCS1_OAEP.new(private_server_key)
key = cipherAES.decrypt(AESKey)
with open("C:\\Users\\Brayd\\Documents\\UMass\\ECE_547\\ML_Encryption\\iv.bin", 'rb') as f:
	iv=f.read()
image_path = "C:\\Users\\Brayd\\Documents\\UMass\\ECE_547\\ML_Encryption\\Encrypted_AES_Images\\Brayden1.enc"
with open(image_path,'rb') as f:
	Encrypted_Face = f.read()
# decrypt
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(Encrypted_Face)
Face_decrypted = unpad(plaintext, AES.block_size)

# integrity check

output_folder = "C:\\Users\\Brayd\\Documents\\UMass\\ECE_547\\ML_Encryption\\Decrypted_AES_Images\\"
output_path = os.path.join(output_folder,"Brayden1.jpg")
with open(output_path, 'wb') as f:
	f.write(Face_decrypted)

facehash = Image.open(output_path)
hashReceived = int.from_bytes(hashlib.sha512(facehash.tobytes()).digest(),byteorder='big')
if signature_hash==hashReceived:
	print("Verified")
else:
	print("Incorrect Hash")


