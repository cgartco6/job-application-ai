import os
from cryptography.fernet import Fernet
import base64

def encrypt_data(data):
    key = os.getenv('ENCRYPTION_KEY').encode()
    f = Fernet(base64.urlsafe_b64encode(key))
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data):
    key = os.getenv('ENCRYPTION_KEY').encode()
    f = Fernet(base64.urlsafe_b64encode(key))
    return f.decrypt(encrypted_data).decode()
