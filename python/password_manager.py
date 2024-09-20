from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.passwords = {}

    def add_password(self, account, password):
        encrypted_password = self.cipher_suite.encrypt(password.encode())
        self.passwords[account] = encrypted_password

    def get_password(self, account):
        encrypted_password = self.passwords.get(account)
        if encrypted_password:
            return self.cipher_suite.decrypt(encrypted_password).decode()
        else:
            return None
