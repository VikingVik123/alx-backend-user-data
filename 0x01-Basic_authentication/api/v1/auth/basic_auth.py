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
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        method 2 decode base_64
        """

        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except (binascii.Error, UnicodeDecodeError):
            return None
        
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        method 2 extract creds
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password