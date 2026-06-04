import base64
from cryptography.fernet import Fernet

def decrypt_text(encrypted_text):

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

    decrypted = cipher.decrypt(
        encrypted_text.encode()
    )

    return decrypted.decode()