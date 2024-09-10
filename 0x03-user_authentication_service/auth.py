#!/usr/bin/env python3
"""
method that takes in a password string arguments and returns bytes
"""
import bcrypt


def _hash_password(password: str) -> str:
    """
    pswd hashing function
    """
    hashed_encoded = password.encode('utf-8')
    hashed = bcrypt.hashpw(hashed_encoded, bcrypt.gensalt())
    return hashed.decode('utf-8')
