#!/usr/bin/env python3
"""
Script to config a bsic flask app
"""
from flask import Flask
from flask import jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'])
def task() -> str:
    """
    A simple GET route that returns a JSON message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
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


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    email = request.form.get["email"]
    password = request.form.get["pass"]
    if not AUTH.valid_login(email, password):
        return(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response

@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    method 2 logout a user and destroy d session id 
    """
    session_id = request.cookies.get("session_id")

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")

@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    method to fetch a user's details
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


if __name__ == '__main__':
    app.run(debug=True)
