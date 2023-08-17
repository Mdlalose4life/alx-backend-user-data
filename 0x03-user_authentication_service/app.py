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
    session_id = request.cookies.get("sesion_id")
    # Find the user with the given session id.
    user = AUTH.get_user_from_session_id(session_Id)
    # abort with 401 statuss if the user is not found
    if user is None:
        abort(403)
    # Otherwise delete the user on that id
    AUTH.destroy_session(user.id)
    # Then redirect
    return redirect("/")
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
