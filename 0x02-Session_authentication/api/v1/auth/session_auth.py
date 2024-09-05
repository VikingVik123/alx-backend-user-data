#!/usr/bin/env python3
"""
Session auth function for the API.
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar, Optional

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    session class creation
    """

