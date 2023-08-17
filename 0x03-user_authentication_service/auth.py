#!/usr/bin/env python3
"""Hash Passsword module
"""
import logging
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound


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


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user based on the given password and email
        """
        try:
            # Search similar email on our existing users.
            self._db.find_user_by(email=email)
            # Raise the ValuError if we find this email
            # already existing.
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            pass
        # Hash the password if it does already not exist.
        new_hashed_password = _hash_password(password)
        # Save the use on the password.
        new_user = self._db.add_user(email, new_hashed_password)
        # Return the new user
        return new_user

    
    def valid_login(self, email: str, password: str) -> bool:
        """
        The function locates user by email, then if the user exists
        We try to match it with existing password with the given email.
        """
        try:
            # Find the user by thier emails.
            user = self._db.find_user_by(email=email)
            if user:
                if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                    return True
        except NoResultFound:
            return False
        return False
