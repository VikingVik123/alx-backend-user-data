#!/usr/bin/env python3
"""
method that takes in a password string arguments and returns bytes
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> str:
    """
    pswd hashing function
    """
    hashed_encoded = password.encode('utf-8')
    hashed = bcrypt.hashpw(hashed_encoded, bcrypt.gensalt())
    return hashed.decode('utf-8')


def _generate_uuid() -> str:
    """
    generate unique id 4 users
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        method to register new users
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pwd = _hash_password(password)
            new_user = self._db.add_user(email, pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        method 2 check 4 valid login credentials
        """
        try:
            user_creds = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'),
                              user_creds.hashed_password.encode('utf-8')):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        creates a session ID 4 the user
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            return session_id
        except NoResultFound:
            return None
