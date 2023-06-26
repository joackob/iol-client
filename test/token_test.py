import os
from src.api.token import Token


def test_token_connect():
    user = os.getenv("IOL_USER") or ""
    password = os.getenv("IOL_PASS") or ""
    token = Token(user=user, password=password)
    assert token.connect() == 200
