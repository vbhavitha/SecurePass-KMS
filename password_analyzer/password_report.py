import re
import math
import hashlib
import requests
from zxcvbn import zxcvbn


# ==========================================
# BASIC PASSWORD ANALYZER
# ==========================================

def analyze_password(password):

    score = 0

    if len(password) >= 8:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"\d", password):
        score += 1

    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        score += 1

    return score


# ==========================================
# ENTROPY CALCULATOR
# ==========================================

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


# ==========================================
# BREACH CHECKER
# ==========================================

def check_password_breach(password):

    sha1 = hashlib.sha1(
        password.encode()
    ).hexdigest().upper()

    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        for line in response.text.splitlines():

            hash_suffix, count = line.split(":")

            if hash_suffix == suffix:
                return int(count)

        return 0

    except Exception:
        return None


# ==========================================
# MAIN PROGRAM
# ==========================================

password = input("Enter Password: ")

# Basic Analysis
basic_score = analyze_password(password)

# zxcvbn Analysis
result = zxcvbn(password)
zxcvbn_score = result["score"]

# Entropy
entropy = calculate_entropy(password)

# Breach Check
breach_count = check_password_breach(password)

# Strength Labels
strength_levels = {
    0: "Very Weak",
    1: "Weak",
    2: "Fair",
    3: "Strong",
    4: "Very Strong"
}

strength = strength_levels[zxcvbn_score]

print("\n")
print("=" * 55)
print("         PASSWORD SECURITY REPORT")
print("=" * 55)

print(f"Password            : {password}")
print(f"Basic Score         : {basic_score}/5")
print(f"zxcvbn Score        : {zxcvbn_score}/4")
print(f"Entropy             : {entropy} bits")
print(f"Strength            : {strength}")
print(f"Estimated Guesses   : {result['guesses']:,}")

# Breach Status
if breach_count is None:

    print("\nBreach Status       : Unable to Check")

elif breach_count > 0:

    print("\nBreach Status       : ⚠ LEAKED")
    print(f"Occurrences         : {breach_count:,}")

else:

    print("\nBreach Status       : ✅ SAFE")
    print("Occurrences         : 0")


# Feedback
feedback = result["feedback"]

if feedback["warning"]:

    print("\nWarning:")
    print(feedback["warning"])

if feedback["suggestions"]:

    print("\nSuggestions:")

    for suggestion in feedback["suggestions"]:
        print("-", suggestion)

print("=" * 55)