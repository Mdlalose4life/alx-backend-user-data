#!/usr/bin/env python3
"""Hash Passsword module
"""
import logging
import uuid
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound


logging.disable(logging.WARNING)


def _hash_password(password: str) -> bytes:
    """
    This function takes in a password and hash it
    so it is not stored in plane text.
    """
    # Convert the password to the bytes.
    byte = password.encode('utf-8')

    # Generate the salt
    salt = bcrypt.gensalt()

    # Hash the password
    Hash = bcrypt.hashpw(byte, salt)

    return Hash


def _generate_uuid() -> str:
    """
    The function creates the uuid.
    Then return the string representation of the uuid.
    """
    return str(uuid.uuid4())


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
                password_bytes = password.encode('utf-8')
                hashed_password = user.hashed_password
                if bcrypt.checkpw(password_bytes, hashed_password):
                    return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        This method creates a session for the user whose email was passed.
        and then, return the return the session ID as a string.
        """
        # Find the user coresponding to the given email.
        try:
            user = self._db.find_user_by(email=email)
        # Except when the user is not found then we return None
        except NoResultFound:
            return None
        # We also return None if the user by email is not found.
        if user is None:
            return None
        # Generate the session ID
        session_id = _generate_uuid()
        # Store the session_id in the database.
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id) -> User
    """
    This funtion finds the user by the corresponding session_id.
    then, it  returns that user or retunrs None, if the
    user is not found.
    """
    # Return None if the session ID is none
    if session_id is None:
        return None
    try:
        # Try and find the user by the sessionID
        user = _db.find_user_by(session_id=session_id)
    # Except, the user is not found by it's session_Id, then
    # return None
    except NoResultFound:
        return None
    # else return the user
    return user
