#!/usr/bin/env python3
""" Flask view that handles all routes for seesion Authantication
"""

import os
from api.v1.app import auth
from api.v1.views import app_views
from api.v1.views import app_views
from models.user import User
from typing import Tuple
from flask import abort, jsonify, request


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login() -> Tuple[str, int]:
    """
    Returns the json presentation of the user object.
    """
    # Getting email and password from the database
    email = request.form.get('email')
    password = request.form.get('password')
    # If email is missing or empty return email 'missing' error
    if not email:
        return jsonify({"error": "email missing"}), 400

    # If password is missing or empty return password not fond error.
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the user
    user = User.search({'email': email})

    # if no user is found, return a no user found for this email error
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    # Validate the email.
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # import auth
    from api.v1.app import auth
    # Otherwise, create a session ID for the User ID
    session_id = auth.create_session(getattr(user[0], 'id'))
    # Return the dictionary representation of the User.
    response = jsonify(user[0].to_json())
    # set the cookie for the response
    response.set_cookie(os.getenv("SESSION_NAME"), session_id)
    # return the response
    return response

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def auth_logout():
    """
    DELETE /api/v1/auth_session/logout
    """
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({}), 200