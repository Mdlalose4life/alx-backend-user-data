#!/usr/bin/env python3
"""
for testing the new 402 error hander.
    1. route must be GET /api/v1/unauthorized
    2. the endpoint must raise 401 error, use abort.
"""
from flask import abort, jsonify


@app.route("/api/v1/unauthorized")
def get_ Unauthorized():
    abort(401)