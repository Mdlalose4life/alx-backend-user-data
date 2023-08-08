#!/usr/bin/env python3
""" Class that managesthe API authantication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    description
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

        for excluded_paths in excluded_paths:
            if excluded_paths.startswith(path):
                return False
            elif path.startswith(excluded_paths):
                return False
            elif excluded_paths[-1] == "*":
                if path.startswith(excluded_paths[-1]):
                    return False

        return True


    def authorization_header(self, request=None) -> str:
        """args:
                request
            returns:
                string
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')

        if header == None:
            return None
        
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """args:
                request
            returns:
                TypeVar
        """
        return None
