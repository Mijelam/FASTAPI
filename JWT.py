import os
from jwt import encode, decode


def createToken(data: dict):
    secret_key = os.getenv("JWT_SECRET")
    token: str = encode(payload=data, key=secret_key, algorithm='HS256')
    return token


def validateToken(token: str):
    secret_key = os.getenv("JWT_SECRET")
    data: dict = decode(token, key=secret_key, algorithms=["HS256"])
    return data
