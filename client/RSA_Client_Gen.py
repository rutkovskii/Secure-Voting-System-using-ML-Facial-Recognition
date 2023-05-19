from Crypto.PublicKey import RSA
import requests
from flask import Flask, request

def key_gen():
    key_pair = RSA.generate(2048)
    private_client_key = key_pair.export_key()
    public_client_key = key_pair.publickey().export_key()
    with open('private_client_msg_key.pem', 'wb') as f:
        f.write(private_client_key)
    with open('public_client_msg_key.pem', 'wb') as f:
        f.write(public_client_key)

if __name__ == "__main__":
    key_gen()



