from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.config import get_settings


settings = get_settings()

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise ValueError(
            "Password must be 72 bytes or fewer."
        )

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(
    password: str,
    hashed_password: str
) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False


def create_access_token(user_id: int) -> str:
    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            return None

        return int(user_id)

    except (JWTError, ValueError, TypeError):
        return None