from flask import (
    Flask,
    render_template,
    request,
    send_file
)
import os
import sqlite3

from password_analyzer.analyzer import analyze_password
from password_analyzer.entropy import calculate_entropy
from password_analyzer.breach_checker import check_password_breach
from password_analyzer.zxcvbn_analyzer import analyze_zxcvbn
from password_generator.generator import generate_password
from kms.encryption import encrypt_text
from kms.decryption import decrypt_text
from kms.rsa_encryption import rsa_encrypt
from kms.rsa_decryption import rsa_decrypt
from kms.key_manager import (
    generate_aes_key,
    generate_rsa_keys
)
from kms.revocation import revoke_key
from werkzeug.utils import secure_filename
from kms.file_encryption import (
    encrypt_file,
    decrypt_file
)
from kms.audit_logger import log_action
from kms.password_history import (
    password_exists,
    save_password
)
from kms.analyzer_history import (
    save_analysis
)


app = Flask(__name__)


@app.route("/")
def home():

    conn = sqlite3.connect("database/kms.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM keys"
    )
    total_keys = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM keys WHERE key_type='AES'"
    )
    aes_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM keys WHERE key_type='RSA'"
    )
    rsa_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM keys
        WHERE status='ACTIVE'
        """
    )
    active_keys = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM keys
        WHERE status='REVOKED'
        """
    )
    revoked_keys = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM password_history
        """
    )
    passwords_generated = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM audit_logs
        """
    )
    audit_events = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT action,
               details,
               created_at
        FROM audit_logs
        ORDER BY log_id DESC
        LIMIT 5
        """
    )
    recent_logs = cursor.fetchall()

    cursor.execute(
        """
        SELECT strength,
               entropy,
               breach
        FROM analyzer_history
        ORDER BY id DESC
        LIMIT 1
        """
    )

    latest_analysis = cursor.fetchone()

    conn.close()

    return render_template(
        "index.html",
        total_keys=total_keys,
        aes_count=aes_count,
        rsa_count=rsa_count,
        active_keys=active_keys,
        revoked_keys=revoked_keys,
        passwords_generated=passwords_generated,
        audit_events=audit_events,
        recent_logs=recent_logs,
        strength=(
            latest_analysis[0]
            if latest_analysis
            else "Not Tested"
        ),

        entropy=(
            latest_analysis[1]
            if latest_analysis
            else "0"
        ),

        breach=(
            latest_analysis[2]
            if latest_analysis
            else "Unknown"
        )
    )



@app.route(
    "/analyzer",
    methods=["GET", "POST"]
)
def analyzer():

    result = None

    if request.method == "POST":

        password = request.form["password"]

        basic_score = analyze_password(password)

        entropy = calculate_entropy(password)

        zxcvbn_result = analyze_zxcvbn(password)

        breach_count = check_password_breach(password)

        result = {
            "basic": basic_score,
            "entropy": entropy,
            "strength": zxcvbn_result["strength"],
            "zxcvbn_score": zxcvbn_result["score"],
            "breach": (
                f"Leaked {breach_count:,} times"
                if breach_count > 0
                else "Safe"
            )
        }
        save_analysis(
            result["strength"],
            result["entropy"],
            result["breach"]
        )

    return render_template(
        "analyzer.html",
        result=result
    )


@app.route("/inventory")
def inventory():

    conn = sqlite3.connect(
        "database/kms.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM keys"
    )

    keys = cursor.fetchall()

    conn.close()

    return render_template(
        "inventory.html",
        keys=keys
    )


@app.route(
    "/generator",
    methods=["GET", "POST"]
)

def generator():

    password = None

    if request.method == "POST":

        length = int(
            request.form["length"]
        )

        while True:

            password = generate_password(
                length
            )

            if not password_exists(
                password
            ):

                save_password(
                    password
                )

                break

    return render_template(
        "generator.html",
        password=password
    )


@app.route(
    "/aes",
    methods=["GET", "POST"]
)
def aes():

    encrypted = None
    decrypted = None

    if request.method == "POST":

        text = request.form["text"]

        if "encrypt" in request.form:

            encrypted = encrypt_text(
                text
            )

        elif "decrypt" in request.form:

            try:
                decrypted = decrypt_text(
                    text
                )

            except:
                decrypted = "Invalid Encrypted Text"

    return render_template(
        "aes.html",
        encrypted=encrypted,
        decrypted=decrypted
    )


@app.route(
    "/rsa",
    methods=["GET", "POST"]
)
def rsa():

    encrypted = None
    decrypted = None

    if request.method == "POST":

        text = request.form["text"]

        if "encrypt" in request.form:

            encrypted = rsa_encrypt(
                text
            )

        elif "decrypt" in request.form:

            try:

                decrypted = rsa_decrypt(
                    text
                )

            except:

                decrypted = (
                    "Invalid RSA Ciphertext"
                )

    return render_template(
        "rsa.html",
        encrypted=encrypted,
        decrypted=decrypted
    )

@app.route(
    "/key-management",
    methods=["GET", "POST"]
)
def key_management():

    message = None

    if request.method == "POST":

        if "generate_aes" in request.form:

            _, filename = generate_aes_key()

            message = (
                f"AES Key Generated: {filename}"
            )

        elif "generate_rsa" in request.form:

            generate_rsa_keys()

            message = (
                "RSA Key Pair Generated"
            )

        elif "revoke" in request.form:

            key_id = request.form["key_id"]

            revoke_key(key_id)

            message = (
                f"Key {key_id} Revoked"
            )

    return render_template(
        "key_management.html",
        message=message
    )

@app.route(
    "/file-encryption",
    methods=["GET", "POST"]
)
def file_encryption():

    message = None
    download_file = None

    if request.method == "POST":

        os.makedirs(
            "uploads",
            exist_ok=True
        )

        os.makedirs(
            "encrypted_files",
            exist_ok=True
        )

        os.makedirs(
            "decrypted_files",
            exist_ok=True
        )
        uploaded_file = request.files["file"]

        filename = secure_filename(
            uploaded_file.filename
        )

        filepath = (
            "uploads/" + filename
        )

        uploaded_file.save(
            filepath
        )

        if "encrypt" in request.form:

            encrypted_path = encrypt_file(
                filepath
            )
            download_file = encrypted_path

            log_action(
                "FILE_ENCRYPT",
                filename
            )

            message = (
                f"Encrypted: {encrypted_path}"
            )

        elif "decrypt" in request.form:

            decrypted_path = decrypt_file(
                filepath
            )
            download_file = decrypted_path

            log_action(
                "FILE_DECRYPT",
                filename
            )

            message = (
                f"Decrypted: {decrypted_path}"
            )

    return render_template(
        "file_encryption.html",
        message=message,
        download_file=download_file
    )

@app.route("/audit-logs")
def audit_logs():

    conn = sqlite3.connect(
        "database/kms.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT action,
               details,
               created_at
        FROM audit_logs
        ORDER BY log_id DESC
        """
    )

    logs = cursor.fetchall()

    conn.close()

    return render_template(
        "audit_logs.html",
        logs=logs
    )

@app.route(
    "/download/<path:filename>"
)
def download_file(filename):

    return send_file(
        filename,
        as_attachment=True
    )

if __name__ == "__main__":

    app.run(debug=True)