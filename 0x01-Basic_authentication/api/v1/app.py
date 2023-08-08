#!/usr/bin/env python3
from flask import jsonify
@app.errorhandler(401)
def unauthorized():
    """
    Eddits the app.py file.
        adding the error handler for the 401 status code
        the response must be.
            1. a JSON: {"error": "Unauthorized"}
            2. status code 401
            3. use jsonify from Flask
    """
    response = {"error": "Unauthorized"}
    return jsonify(response), 401