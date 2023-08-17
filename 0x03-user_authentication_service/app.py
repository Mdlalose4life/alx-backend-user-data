#!/usr/bin/env python3
"""This module initializes a basic app
"""
import logging

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
logging.disable(logging.WARNING)

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def Hello():
    """
    returns the message in json format
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
    """
    The Function that implements the Post /users
    """
    # Get email form
    email = request.form.get("email")
    # Get pasword fom
    password = request.form.get("password")
    try:
        # Register the user
        AUTH.register_user(email, password)
        # Alert that the user with the given email was created.
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({{"message": "email already registered"}}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """
    Funtion to that respond the the POST /session route
    """
    # Request the email
    email = request.form.get("email")
    # Request the password
    password = request.form.get("password")
    # Abort if emeil or passwor is not correct.
    if not AUTH.valid_login(email, password):
        abort(401)
    # Create the session_id
    session_id = AUTH.create_session(email)
    # Send alert if the session ID ceated succesfully.
    respond = jsonify({"email": email, "message": "logged in"})
    # Set cookie for the sesion_id
    respond.set_cookie("session_id", session_id)
    return respond


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    Logging out the user.
    """
    # Send a request for session id
    session_id = request.cookies.get("session_id")
    # Find the user with the given session id.
    user = AUTH.get_user_from_session_id(session_id)
    # abort with 401 statuss if the user is not found
    if user is None:
        abort(403)
    # Otherwise delete the user on that id
    AUTH.destroy_session(user.id)
    # Then redirect home
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    This methods responds to GET /profile
    """
    # Let's get the session ID
    session_id = request.cookies.get("session_id")
    # find a user by session ID
    user = AUTH.get_user_from_session_id(session_id)
    # if the user or session id does not exist respond with 403.
    if user is None:
        abort(403)
    # if the user exists, respond with 200 status
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    resets the password
    """
    # Send a request to get an email
    email = request.form.get("email")
    # If the email is not registered then return a 403 error
    try:
        # Try to generate the reset token for the email.
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        # if the email is not in a database, raise 403 error.
        abort(403)
    return jsonify({"email": email, "reset_token": reset token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
