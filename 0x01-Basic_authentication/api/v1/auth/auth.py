#!/usr/bin/env python3
"""
Authentication module
"""
import re
from flask import request
from typing import List, Union, TypeVar


class Auth:
    """
    Authentication class.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        func 2 check authorization
        """
        pass

    def authorization_header(self, request=None) -> str:
        """
        checks for authorization
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        checks 4 current user
        """
        return None
