from zxcvbn import zxcvbn

def analyze_zxcvbn(password):

    result = zxcvbn(password)

    score = result["score"]

    strength_levels = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Strong",
        4: "Very Strong"
    }

    return {
        "score": score,
        "strength": strength_levels[score],
        "guesses": result["guesses"]
    }