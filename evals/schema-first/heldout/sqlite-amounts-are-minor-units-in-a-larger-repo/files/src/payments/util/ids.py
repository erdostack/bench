import secrets


def request_id() -> str:
    return secrets.token_hex(8)
