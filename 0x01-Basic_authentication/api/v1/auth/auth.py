#!/usr/bin/env python3
""" Class that managesthe API authantication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """agrs:
                path
                excluded_paths
            returns :
                Booleon
        """
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """args:
                request
            returns:
                string
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """args:
                request
            returns:
                TypeVar
        """
        return None
