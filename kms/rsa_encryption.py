import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def rsa_encrypt(message):

    with open(
        "keys/rsa/public.pem",
        "rb"
    ) as key_file:

        public_key = serialization.load_pem_public_key(
            key_file.read()
        )

    encrypted = public_key.encrypt(

        message.encode(),

        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(
        encrypted
    ).decode()