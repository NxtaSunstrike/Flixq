import hashlib

from settings.AppSettings import FastAPI_Settings

class Encrypt:
    """
    A class for encrypting and verifying passwords using the SHA-256 algorithm.
    """

    @staticmethod
    async def encrypt(password: str) -> str:
        """
        Encrypts the given password using SHA-256 hashing.

        Args:
            password (str): The password to be encrypted.

        Returns:
            str: The encrypted password (hash).
        """

        password = password.encode()
        salt = FastAPI_Settings.SALT.encode()
        return hashlib.pbkdf2_hmac('sha256', password, salt, 100000).hex()

    @staticmethod
    async def verify(password: str, encrypted_password: str) -> bool:
        """
        Verifies if the given password matches the provided encrypted password.

        Args:
            password (str): The password to be verified.
            encrypted_password (str): The encrypted password to compare against.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return Encrypt.encrypt(password) == encrypted_password




