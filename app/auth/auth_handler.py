import time
from typing import Dict

import jwt
#from decouple import config


JWT_SECRET="et26e02833ef2b051fec2wf9ae0a45e992e3dccf9e6e770"
JWT_ALGORITHM="HS256"
#JWT_SECRET = config("JWT_SECRET")
#JWT_ALGORITHM = config("JWT_ALGORITHM")


def token_response(token: str):
    return {
        "access_token": token
    }


def sign_jwt(user_id: str, expiration = 600) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decode_jwt(token: str, type = "check") -> dict:
    if type == "logout":
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = decoded_token["user_id"]
        token = jwt.encode({"user_id": user_id, "expires": -600}, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token_response(token)
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}