#!/usr/bin/env python3
"""
Script to config a bsic flask app
"""
from flask import Flask
from flask import jsonify, request, abort
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'])
def task():
    """
    A simple GET route that returns a JSON message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """
    method to return user credentials
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.run(debug=True)
