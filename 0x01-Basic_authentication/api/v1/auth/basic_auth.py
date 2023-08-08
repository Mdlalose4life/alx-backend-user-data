#!/usr/bin/env python3
"""Module for basic authentication
"""
import base64
import binascii
from models.user import User
from .auth import Auth


class BasicAuth(Auth):
    """
    Basic Authantication class
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        extracts the base64 part of the Authorization header.
         Args:
            authorization_header (str): The Authorization header string.
        Returns:
            str: The Base64 part of the Authorization header, or None if the
            header is invalid.
        """
        if authorization_header is None or not \
                isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split('Basic ')[1].strip()
