import math

def calculate_entropy(password):

    charset = 0

    if any(c.islower() for c in password):
        charset += 26

    if any(c.isupper() for c in password):
        charset += 26

    if any(c.isdigit() for c in password):
        charset += 10

    if any(not c.isalnum() for c in password):
        charset += 32

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)

    return round(entropy, 2)