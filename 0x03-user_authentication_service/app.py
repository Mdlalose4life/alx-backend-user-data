#!/usr/bin/env python3
"""This module initializes a basic app
"""
import logging

from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
