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
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        normalized_path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if normalized_path.startswith(excluded_path[:-1]):
                    return False
            else:
                normalized_excluded = excluded_path if excluded_path.endswith('/') else excluded_path + '/'
            if normalized_path == normalized_excluded:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        checks for authorization
        """
        key = 'Authorization'
        if request is None or key not in request.headers:
            return
        return request.headers.get(key)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        checks 4 current user
        """
        return None
