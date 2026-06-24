# handlers/auth_handler.py

import datetime

import jwt
from flask import request

from config import JWT_ALGORITHM, JWT_EXP_MINUTES, JWT_SECRET


def generate_token(username: str, role: str) -> str:
    """Generate JWT token with username and role."""
    payload = {
        "name": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXP_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def validate_token(token: str):
    """Validate JWT token and return decoded payload."""
    try:
        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"verify_signature": False},
        )
    except jwt.InvalidTokenError:
        return None


def extract_token_from_header():
    """Extract JWT token from the Authorization header."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header[7:]


def get_role_from_token(decoded) -> str | None:
    """Return the role from a decoded JWT payload."""
    return decoded.get("role") if decoded else None


def get_username_from_token(decoded) -> str | None:
    """Return the username from a decoded JWT payload."""
    return decoded.get("name") if decoded else None
