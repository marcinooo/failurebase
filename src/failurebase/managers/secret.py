"""Secrets manager module."""

from cryptography.fernet import Fernet
from passlib.context import CryptContext


class SecretManager:
    """
    Manager to control secrets.
    There are two types of secrets in database:
    1). Api-Key - his encrypted value is stored in database,
    2). Client's Secret - individual client's secret, which hash value is stored in database.
    """

    def __init__(self, secret_key):
        self.secret_key = secret_key

        self.crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.fernet = Fernet(secret_key.encode('utf-8'))

    def encrypt(self, data):
        """Encrypts given data."""

        return self.fernet.encrypt(data.encode('utf-8')).decode('utf-8')

    def decrypt(self, data):
        """Decrypts given data."""

        return self.fernet.decrypt(data.encode('utf-8')).decode('utf-8')

    def verify_hash(self, plain_secret, hashed_secret):
        """Verifies if given secret match with hash."""

        return self.crypt_context.verify(plain_secret, hashed_secret)

    def get_hash(self, secret):
        """Generates hash from given secret."""

        return self.crypt_context.hash(secret)
