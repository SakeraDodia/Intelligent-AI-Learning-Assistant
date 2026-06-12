from jose import jwt

SECRET_KEY = "ai_learning_secret"

ALGORITHM = "HS256"


def create_access_token(data):

    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token