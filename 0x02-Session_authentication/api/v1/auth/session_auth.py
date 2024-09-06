#!/usr/bin/env python3
"""
Session auth function for the API.
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar, Optional
from uuid import uuid4
import os

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    session class creation
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        method 2 create session
        """

        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        method 2 extract user_id from session
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def session_cookie(self, request=None) -> Optional[str]:
        """
        method 2 return session cookie
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)