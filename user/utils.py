import re


def pattern_password(password):
    if re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.*\s).{8,}$', password):
        return True
    else:
        return False