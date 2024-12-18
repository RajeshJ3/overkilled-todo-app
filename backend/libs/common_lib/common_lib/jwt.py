from datetime import datetime, timedelta, timezone

from os import environ as env

import jwt

SECRET_KEY = env["SECRET_KEY"]
ACCESS_TOKEN_TTL = env.get("ACCESS_TOKEN_TTL", 43200)
ALGORITHM = env.get("ALGORITHM", "HS256")


def get_access_token(to_encode: dict, expires_delta: timedelta | None = None) -> str:

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_TTL))

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(access_token: str) -> dict:
    return jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
