#!/usr/bin/env python3
"""This module initializes a basic app
"""

from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def Hello():
    """
    returns the message in json format
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
