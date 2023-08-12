#!/usr/bin/env python3
"""Module for basic authentication
"""
from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """
    Sesion Auth Class that inherits from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create sesssion Method creates a Sesion ID for user ID
        """
        # if user id is a string
        if type(user_id) is not str:
            return None
        else:
            # Generate the Session ID for the user
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            # Return Session ID
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns the User ID based on a Session ID
        """
        # If session Id is none return None
        if session_id is None:
            return None
        # Return None if if session ID is not a string
        if type(session_id) is not str:
            return None
        else:
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        Retuns the user instance based on the cookie value
        """
        # Retrieves the session ID cookies from the reqest
        session_id = self.session_cookie(request)
        # Look for the current user based on the use_id.
        user_id = self.user_id_for_session_id(session_id)
        # Retrives the user instance on the database based on the user ID
        user = User.get(user_id)
        # Retuns the user instance
        return user
    
    def destroy_session(self, request=None):
        """
        Method to delete the user session/logout.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        # If the request is equal to None return False
        if (request is None or session_id is None) or use_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
