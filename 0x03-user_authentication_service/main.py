#!/usr/bin/env python3
"""
Method to test our functions
"""

import requests


def register_user(email: str, password: str) -> None:
    """ Register a new user """
    response = requests.post(f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    print(f"User {email} successfully registered.")

def log_in_wrong_password(email: str, password: str) -> None:
    """ Try logging in with wrong password """
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401
    print(f"Log in attempt with wrong password for {email} correctly rejected.")

def log_in(email: str, password: str) -> str:
    """ Log in with correct credentials and return session ID """
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    print(f"User {email} logged in successfully. Session ID: {session_id}")
    return session_id

def profile_unlogged() -> None:
    """ Try accessing profile without being logged in """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403
    print("Profile access correctly blocked for unauthenticated user.")

def profile_logged(session_id: str) -> None:
    """ Access profile while logged in with a valid session ID """
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()
    print(f"Profile accessed successfully. User email: {response.json()['email']}")

def log_out(session_id: str) -> None:
    """ Log out by ending the session """
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}
    print(f"User logged out successfully. Session ID: {session_id}")

def reset_password_token(email: str) -> str:
    """ Request a reset password token """
    response = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    assert reset_token is not None
    print(f"Password reset token for {email}: {reset_token}")
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Update the password using reset token """
    response = requests.put(f"{BASE_URL}/reset_password", data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}
    print(f"Password for {email} updated successfully.")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)