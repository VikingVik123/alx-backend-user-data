#!/usr/bin/env python3
"""
Authentication module
"""
from flask import requests
from typing import List, Union, TypeVar


class Auth:


    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
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
