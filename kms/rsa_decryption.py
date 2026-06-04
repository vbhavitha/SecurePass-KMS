import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def rsa_decrypt(encrypted_text):

    with open(
        "keys/rsa/private.pem",
        "rb"
    ) as key_file:

        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    encrypted = base64.b64decode(
        encrypted_text
    )

    decrypted = private_key.decrypt(

        encrypted,

        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted.decode()