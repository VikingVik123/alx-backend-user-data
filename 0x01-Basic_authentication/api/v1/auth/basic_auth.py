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
    pass
