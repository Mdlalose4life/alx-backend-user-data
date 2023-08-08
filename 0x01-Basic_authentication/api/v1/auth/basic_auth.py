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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        decodes the value of base64 string
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded = base64.b64decode(
                base64_authorization_header,
                validate=True
            )
            return decoded.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user email and password from Base64 decoded values
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        try:
            email, password = decoded_base64_authorization_header.split(':', 1)
        except ValueError:
            return None, None

        return email, password
