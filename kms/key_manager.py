import os

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from kms.audit_logger import log_action


# ==========================================
# AES-256 KEY GENERATION
# ==========================================

import sqlite3
from datetime import datetime


def generate_aes_key():

    conn = sqlite3.connect(
        "database/kms.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM keys
        WHERE key_type='AES'
        """
    )

    count = cursor.fetchone()[0]

    key_number = count + 1

    filename = f"aes_key_{key_number}.key"

    key = os.urandom(32)

    with open(
        f"keys/aes/{filename}",
        "wb"
    ) as file:

        file.write(key)

    cursor.execute(
        """
        UPDATE keys
        SET status='INACTIVE'
        WHERE key_type='AES'
        """
    )

    cursor.execute(
        """
        INSERT INTO keys
        (
            key_name,
            key_type,
            created_at,
            status
        )
        VALUES (?, ?, ?, ?)
        """,

        (
            filename,
            "AES",
            datetime.now().isoformat(),
            "ACTIVE"
        )
    )
    log_action(
    "GENERATE_AES",
    filename
)

    conn.commit()
    conn.close()

    return key, filename


# ==========================================
# RSA-2048 KEY PAIR GENERATION
# ==========================================

def generate_rsa_keys():

    conn = sqlite3.connect(
        "database/kms.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM keys
        WHERE key_type='RSA'
        """
    )

    count = cursor.fetchone()[0]

    key_number = count + 1

    key_name = f"RSA_KEY_{key_number}"

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    with open(
        "keys/rsa/private.pem",
        "wb"
    ) as f:

        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    with open(
        "keys/rsa/public.pem",
        "wb"
    ) as f:

        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    cursor.execute(
        """
        UPDATE keys
        SET status='INACTIVE'
        WHERE key_type='RSA'
        """
    )

    cursor.execute(
        """
        INSERT INTO keys
        (
            key_name,
            key_type,
            created_at,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            key_name,
            "RSA",
            datetime.now().isoformat(),
            "ACTIVE"
        )
    )
    log_action(
    "GENERATE_RSA",
    key_name
)

    conn.commit()
    conn.close()

    return private_key, public_key


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    # Generate AES Key
    aes_key, filename = generate_aes_key()

    print("\nAES-256 Key Generated Successfully")
    print("Key File:", filename)
    print("Key Size:", len(aes_key), "bytes")

    # Generate RSA Key Pair
    private_key, public_key = generate_rsa_keys()

    print("\nRSA-2048 Key Pair Generated Successfully")

    print("\nGenerated Files:")

    print("keys/aes/aes.key")
    print("keys/rsa/private.pem")
    print("keys/rsa/public.pem")