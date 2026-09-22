from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    if additional_claims:
        payload.update(additional_claims)

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def create_refresh_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=30)

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError as exc:
        raise ValueError("Invalid or expired token") from exc


def get_token_subject(token: str) -> str:
    payload = decode_token(token)

    subject = payload.get("sub")

    if not subject:
        raise ValueError("Token subject missing")

    return str(subject)


def is_token_expired(token: str) -> bool:
    try:
        payload = decode_token(token)

        exp = payload.get("exp")

        if exp is None:
            return True

        expiration_time = datetime.fromtimestamp(exp, tz=timezone.utc)

        return expiration_time < datetime.now(timezone.utc)

    except Exception:
        return True


def create_password_reset_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    payload = {"sub": email, "exp": expire, "type": "password_reset"}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_password_reset_token(token: str) -> str:
    payload = decode_token(token)

    token_type = payload.get("type")

    if token_type != "password_reset":
        raise ValueError("Invalid password reset token")

    email = payload.get("sub")

    if not email:
        raise ValueError("Email missing in token")

    return str(email)


def create_email_verification_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=24)

    payload = {"sub": email, "exp": expire, "type": "email_verification"}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_email_verification_token(token: str) -> str:
    payload = decode_token(token)

    token_type = payload.get("type")

    if token_type != "email_verification":
        raise ValueError("Invalid email verification token")

    email = payload.get("sub")

    if not email:
        raise ValueError("Email missing in token")

    return str(email)
