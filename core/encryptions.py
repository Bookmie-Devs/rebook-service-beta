from decouple import config
from cryptography.fernet import Fernet, InvalidToken

encryption_key: str = config('ENCRYPTION_KEY', cast=str)

ENCRYPTION_KEY = encryption_key.encode()

crypt = Fernet(key=ENCRYPTION_KEY)


def encrypt_data(data) -> str:
    return crypt.encrypt(str(data).encode()).decode()


def decrypt_data(data: bytes | str) -> str | int:
    try:
        return crypt.decrypt(data).decode()
    except:
        return 000



