#!/usr/bin/env python3
"""
method that takes in a password string arguments and returns bytes
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> str:
    """
    pswd hashing function
    """
    hashed_encoded = password.encode('utf-8')
    hashed = bcrypt.hashpw(hashed_encoded, bcrypt.gensalt())
    return hashed.decode('utf-8')


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        method to register new users
        """
        existing_email = self._db.find_user_by(email=email)
        if email == existing_email:
            raise ValueError(f"User {email} already exists")

        else:
            pwd = _hash_password(password)
            new_user = self._db.add_user(email, pwd)
            return new_user
