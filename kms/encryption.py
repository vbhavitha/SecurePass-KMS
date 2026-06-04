import base64
from cryptography.fernet import Fernet

def encrypt_text(message):

    with open(
        "keys/aes/aes.key",
        "rb"
    ) as f:

        aes_key = f.read()

    fernet_key = base64.urlsafe_b64encode(
        aes_key
    )

    cipher = Fernet(
        fernet_key
    )

    encrypted = cipher.encrypt(
        message.encode()
    )

    return encrypted.decode()