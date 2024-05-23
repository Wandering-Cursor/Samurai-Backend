import hashlib
import secrets


def hash_value(value: str) -> str:
    return hashlib.sha512(value.encode()).hexdigest()


def check_hash(value: str, hashed_value: str) -> bool:
    return hash_value(value) == hashed_value


def generate_random_string(length: int = 32) -> str:
    return secrets.token_hex(length)
