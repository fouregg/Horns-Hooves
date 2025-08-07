from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError


def create_password_reset_token(email: str) -> str:
    expires = datetime.now() + timedelta(hours=1)
    to_encode = {"sub": email, "exp": expires, "type": "password_reset"}
    return jwt.encode(to_encode, "admin", algorithm="HS256")


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, "admin", algorithms=["HS256"])
        if payload.get("type") != "password_reset":
            return None
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None
