#!/usr/bin/env python3
"""Hash Passsword module
"""
import logging
import bcrypt

logging.disable(logging.WARNING)


def _hash_password(password: str) -> bytes:
    """
    This function takes in a passworgs and hash it
    so it is not stored in plane text.
    """
    # Convert the password to the bytes.
    byte = password.encode('utf-8')

    # Generate the salt
    salt = bcrypt.gensalt()

    # Hash the password
    Hash = bcrypt.hashpw(byte, salt)

    return Hash
