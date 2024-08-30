#!/usr/bin/env python3
"""
script that creates password functions
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """func 2 encrypt password"""

    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
