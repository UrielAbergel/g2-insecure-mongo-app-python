# services/user_service.py

import hashlib
import os

from models.init_db import users_collection

HASH_ITERATIONS = 100_000


def hash_password(password: str, salt: bytes | None = None) -> str:
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, HASH_ITERATIONS)
    return salt.hex() + ":" + dk.hex()


def verify_password(password: str, stored_hash: str) -> bool:
    if ":" in stored_hash:
        salt_hex, _ = stored_hash.split(":", 1)
        salt = bytes.fromhex(salt_hex)
        return hash_password(password, salt) == stored_hash
    return stored_hash == hashlib.sha1(password.encode()).hexdigest()


def validate_user(username: str, password: str) -> bool:
    """Check if a user exists and password matches."""
    user = users_collection.find_one({"username": username})
    if not user:
        return False

    return verify_password(password, user.get("credentialHash", ""))


def get_user_role(username: str) -> str | None:
    """Return the role associated with a given user, if exists."""
    user = users_collection.find_one({"username": username})
    return user.get("role") if user else None


def create_user(username: str, password: str, role: str = "reader") -> bool:
    """Create a new user with a given role (default: reader)."""
    if users_collection.find_one({"username": username}):
        return False

    new_user = {
        "username": username,
        "credentialHash": hash_password(password),
        "role": role if role in ["reader", "writer"] else "reader",
    }

    users_collection.insert_one(new_user)
    return True
