#!/usr/bin/env python3
"""
Session auth function for the API.
"""
from typing import Tuple, TypeVar, Optional
from uuid import uuid4
import os
from flask import jsonify, request, abort
from api.v1.views import app_views
from .auth import Auth
from api.v1.app import auth
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
    
    def current_user(self, request=None) -> Optional[User]:
        """
        Retrieve a User instance based on the session cookie.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)
    
    @app_views.route('/auth_session/login/', methods=['POST'], strict_slashes=False)
    def login():
        """
        Route to handle user login and create session.
        """

        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            return jsonify({"error": "email missing"}), 400

        if not password:
            return jsonify({"error": "password missing"}), 400

        try:
            users = User.search({"email": email})
        except Exception as e:
            return jsonify({"error": "no user found for this email"}), 404

        if not users or len(users) == 0:
            return jsonify({"error": "no user found for this email"}), 404

        user = users[0]

        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        session_id = auth.create_session(user.id)
        if not session_id:
            abort(500)

        response = jsonify(user.to_json())

        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        response.set_cookie(session_name, session_id)

        return response