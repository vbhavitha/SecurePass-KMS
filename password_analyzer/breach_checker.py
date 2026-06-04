import hashlib
import requests

def check_password_breach(password):

    sha1 = hashlib.sha1(
        password.encode()
    ).hexdigest().upper()

    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    response = requests.get(url)

    for line in response.text.splitlines():

        hash_suffix, count = line.split(":")

        if hash_suffix == suffix:
            return int(count)

    return 0