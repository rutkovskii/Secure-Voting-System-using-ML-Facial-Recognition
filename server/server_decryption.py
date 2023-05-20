from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import hashlib
import json

def decrypt_data(data):
    with open('private_server_msg_key.pem', 'rb') as f:
        private_server_key = RSA.importKey(f.read())
    with open('public_client_msg_key.pem', 'rb') as f:
        public_client_key = RSA.importKey(f.read())

    # Convert data to string with json.dumps, then to bytes
    message = json.loads(data)

    # receive digital signature and apply public client key
    signature_hash_msg = pow(message.get("digital_signature"), public_client_key.e, public_client_key.n)
    #print(signature_hash_msg)
    #decrypt AES key
    mode = AES.MODE_CBC
    keyLen = 32
    ivLen = AES.block_size

    cipherAES = PKCS1_OAEP.new(private_server_key)
    key = cipherAES.decrypt(message.get('encrypted_key').to_bytes(((message.get('encrypted_key')).bit_length() + 7) // 8,'big'))
    iv = message.get('iv').to_bytes(((message.get('iv')).bit_length() + 7) // 8,'big')
    Encrypted_message = message.get('msg_encrypted').to_bytes(((message.get('msg_encrypted')).bit_length() + 7) // 8,'big')

    # decrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(Encrypted_message)
    message_decrypted = unpad(plaintext, AES.block_size)

    # integrity check
    hashReceived = int.from_bytes(hashlib.sha512(message_decrypted).digest(),byteorder='big')
    if signature_hash_msg==hashReceived:
        verified = 1
    else:
        verified = 0
    #print(bytes.decode((message_decrypted),'utf-8'))
    return{
        "verified":verified,
        'msg_decrypted':json.loads(bytes.decode((message_decrypted),'utf-8'))
    }

'''
# testing
# open encryped json
with open('../client/json_test.json') as user_file: # replace with json open
  f = user_file.read()
# decrypt json
d_data=decrypt_data(f)
# load the json data
decrypted_data = json.dumps(d_data)
decrypted_data = json.loads(decrypted_data)
# print the first json 'verified' 0 or 1 for hash data
print(decrypted_data.get('verified'))
# get the json inside of this json of user input data
data=decrypted_data.get('msg_decrypted').replace("'",'"')
user_data = json.loads(data) # load the json of user data
print(user_data.get("image_data")) # can print any json of user data attributed
'''




