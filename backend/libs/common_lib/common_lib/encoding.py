def encode_str(string: str) -> bytes:
    return string.encode("utf-8")


def decode_bytes(string: bytes) -> str:
    return string.decode("utf-8")
