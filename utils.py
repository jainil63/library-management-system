import jwt
from jwt.exceptions import InvalidTokenError


def create_token(id, username, isadmin):
    payload = {
        "id": id,
        "username": username,
        "isadmin": isadmin
    }
    token = jwt.encode(payload=payload, key="my_secret_key", algorithm="HS256")
    return token


def verify_and_decode_token(token):
    try:
        payload = jwt.decode(token, key="my_secret_key", algorithms=["HS256", ])
        return payload
    except InvalidTokenError as e:
        return False
