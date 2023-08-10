#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

AUTH_TYPE = os.getenv("AUTH_TYPE")


if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def before_request():
    """
    """
    if auth is None:
        pass
    else:
        excluded_list = ['/api/v1/status/',
                         '/api/v1/unauthorized/', '/api/v1/forbidden/']

        if auth.require_auth(request.path, excluded_list):
            if auth.authorization_header(request) is None:
                abort(401, description="Unauthorized")
            if auth.current_user(request) is None:
                abort(403, description="Forbidden")

        user = auth.current_user(request)
        if user is None:
            abort(403)

        request.current_user = user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(403)
def forbidden(error) -> str:
    """Error Forbidden
    """
    response = {"error": "Forbidden"}
    return jsonify(response), 403


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Error: Unauthorizes
    """
    status = {"error": "Unauthorized"}
    return jsonify(status), 401


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
