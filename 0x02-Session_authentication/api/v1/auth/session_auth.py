#!/usr/bin/env python3
"""Module for basic authentication
"""
from .auth import Auth
from uuid import uuid4


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
            sessison_id = str(uuid4())
            self.user_id_by_session_id[sessison_id] = user_id
            # Return Session ID
            return sessison_id
