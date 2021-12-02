from typing import Optional

import hashlib
import hmac

import base64


SEKRET_KEY = 'b7e53aa9cb63871f847ab88a849434b6a498a47516cd935009a9a15e77b1b2c0'
PASSWORD_SALT = 'a94fa879941c5377d6a4e6b4c5447ce81ad54355e10597a40efc9f5e6f9b3274'


def sign_data(data: str) -> str:
    return hmac.new(
        SEKRET_KEY.encode(), msg=data.encode(), digestmod=hashlib.sha256
        ).hexdigest().upper()


def get_username_from_signed_string(username_signed: str) -> Optional[str]:
    username_base64, sign = username_signed.split('.')
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)

    if hmac.compare_digest(valid_sign, sign):
        return username

