from cryptography.fernet import Fernet

class DataProtection:
    def __init__(self, key=None):
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_data(self, data):
        return self.cipher.encrypt(data.encode())

    def decrypt_data(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data).decode()
