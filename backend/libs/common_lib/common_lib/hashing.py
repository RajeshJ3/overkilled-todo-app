import bcrypt

from common_lib.encoding import encode_str, decode_bytes


def get_hashed_password(password: str) -> str:
    hash_bytes = bcrypt.hashpw(encode_str(password), bcrypt.gensalt())
    return decode_bytes(hash_bytes)


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(encode_str(password), encode_str(hashed_password))
