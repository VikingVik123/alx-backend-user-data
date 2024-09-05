#!/usr/bin/env python3
"""
Session auth function for the API.
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar, Optional
from uuid import uuid4

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



