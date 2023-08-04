from cryptography.fernet import Fernet
from passlib.context import CryptContext


class SecretManager:

    def __init__(self, secret_key):
        self.secret_key = secret_key

        self.crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.fernet = Fernet(secret_key.encode('utf-8'))

    def encrypt(self, data):
        return self.fernet.encrypt(data.encode('utf-8')).decode('utf-8')

    def decrypt(self, data):
        return self.fernet.decrypt(data.encode('utf-8')).decode('utf-8')

    def verify_hash(self, plain_secret, hashed_secret):
        return self.crypt_context.verify(plain_secret, hashed_secret)

    def get_hash(self, secret):
        return self.crypt_context.hash(secret)
