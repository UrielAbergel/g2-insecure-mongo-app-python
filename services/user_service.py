# services/user_service.py

import hashlib

from models.init_db import users_collection


def hash_password(password: str) -> str:
    return hashlib.sha1(password.encode()).hexdigest()


def validate_user(username: str, password: str) -> bool:
    """Check if a user exists and password matches."""
    user = users_collection.find_one({"username": username})
    if not user:
        return False

    return user.get("passwordHash") == hash_password(password)


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
        "passwordHash": hash_password(password),
        "role": role if role in ["reader", "writer"] else "reader",
    }

    users_collection.insert_one(new_user)
    return True
