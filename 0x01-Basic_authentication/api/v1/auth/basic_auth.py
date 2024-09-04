#!/usr/bin/env python3
"""
Basic auth function for the API.
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    creates BasicAuth class
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        method for base64 auth
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        base64_part = authorization_header[len("Basic "):]
        return base64_part