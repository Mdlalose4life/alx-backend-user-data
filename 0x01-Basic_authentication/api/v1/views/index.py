#!/usr/bin/env python3
"""
Index view Module
"""
from flask import abort, jsonify
from api.v1.views import app_views

@app_views.route("/unauthorized", methods=['GET'], strict_slashes=False)
def get_ Unauthorized() -> str:
    """
    for testing the new 402 error hander.
        1. route must be GET /api/v1/unauthorized
        2. the endpoint must raise 401 error, use abort.
    """
    abort(401, description="Unauthorized")