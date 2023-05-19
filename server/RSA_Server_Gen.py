from Crypto.PublicKey import RSA
import requests
from flask import Flask, request

def key_gen():
    key_pair = RSA.generate(2048)
    private_server_key = key_pair.export_key()
    public_server_key = key_pair.publickey().export_key()
    with open('private_server_key.pem', 'wb') as f:
        f.write(private_server_key)
    with open('public_server_key.pem', 'wb') as f:
        f.write(public_server_key)

if __name__ == "__main__":
    key_gen()
