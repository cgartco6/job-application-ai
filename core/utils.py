from cryptography.fernet import Fernet

def encrypt_data(data):
    key = os.getenv('ENCRYPTION_KEY')
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data):
    key = os.getenv('ENCRYPTION_KEY')
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()
