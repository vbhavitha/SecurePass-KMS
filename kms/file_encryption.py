import os
import base64

from cryptography.fernet import Fernet


def load_cipher():

    with open(
        "keys/aes/aes.key",
        "rb"
    ) as f:

        aes_key = f.read()

    fernet_key = base64.urlsafe_b64encode(
        aes_key
    )

    return Fernet(
        fernet_key
    )


def encrypt_file(filepath):

    cipher = load_cipher()

    with open(
        filepath,
        "rb"
    ) as file:

        data = file.read()

    encrypted = cipher.encrypt(
        data
    )

    encrypted_path = (
        "encrypted_files/"
        + os.path.basename(filepath)
        + ".enc"
    )

    with open(
        encrypted_path,
        "wb"
    ) as file:

        file.write(encrypted)

    return encrypted_path


def decrypt_file(filepath):

    cipher = load_cipher()

    with open(
        filepath,
        "rb"
    ) as file:

        encrypted = file.read()

    decrypted = cipher.decrypt(
        encrypted
    )

    filename = os.path.basename(
        filepath
    ).replace(".enc", "")

    decrypted_path = (
        "decrypted_files/"
        + filename
    )

    with open(
        decrypted_path,
        "wb"
    ) as file:

        file.write(decrypted)

    return decrypted_path