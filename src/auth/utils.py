from datetime import datetime, timedelta, timezone
import jwt
import settings


def decode_access_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
