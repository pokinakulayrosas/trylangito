import secrets

def createToken():
    token = secrets.token_urlsafe(32)
    return token     