#!/usr/bin/env python3
"""auth module"""
from flask import request
from typing import TypeVar, List


class Auth:
    """manage the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        if (path is None or
            excluded_paths is None or
            len(excluded_paths) == 0
        ):
            return True
    
        if path.endswith('/'):
            for idx in range(len(excluded_paths)):
                if excluded_paths[idx].endswith("/"):
                    continue
                else:
                    excluded_paths[idx] = f"{excluded_paths[idx]}/"
        else:
            for idx in range(len(excluded_paths)):
                if excluded_paths[idx].endswith("/"):
                    excluded_paths[idx] = excluded_paths[idx][:-1]
                else:
                    continue

        if path in excluded_paths:
            return False
        else:
            return True


    def authorization_header(self, request=None) -> str:
        """auth header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
