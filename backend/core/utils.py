import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings

def get_encryption_key():
    """Derive encryption key from environment variable"""
    password = os.getenv('ENCRYPTION_KEY', 'default-secret-key').encode()
    salt = b'salt_'  # Should be unique and stored securely
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

def encrypt_data(data):
    """Encrypt data using Fernet symmetric encryption"""
    if isinstance(data, str):
        data = data.encode()
    f = Fernet(get_encryption_key())
    return f.encrypt(data)

def decrypt_data(encrypted_data):
    """Decrypt data using Fernet symmetric encryption"""
    f = Fernet(get_encryption_key())
    return f.decrypt(encrypted_data).decode()
