#!/usr/bin/env python3
"""auth module"""
from flask import request
from typing import TypeVar, List


class Auth:
    """manage the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require auth method

        Args:
            path (str): api path
            excluded_paths (List[str]): list of excluded api path

        Returns:
            bool: True if path not in excluded_path or False
        """
        if (
            path is None or
            excluded_paths is None or
            len(excluded_paths) == 0
        ):
            return True

        if path.endswith('/'):
            for idx in range(len(excluded_paths)):
                if excluded_paths[idx].endswith("/"):
                    continue
                elif excluded_paths[idx].endswith("*"):
                    idx_last_el = (excluded_paths[idx].split("/"))[-1]
                    path_last_el = path.split("/")[-2]
                    if path_last_el.startswith(idx_last_el[:-1]):
                        excluded_paths[idx] = path
                else:
                    excluded_paths[idx] = f"{excluded_paths[idx]}/"
        else:
            for idx in range(len(excluded_paths)):
                if excluded_paths[idx].endswith("/"):
                    excluded_paths[idx] = excluded_paths[idx][:-1]
                elif excluded_paths[idx].endswith("*"):
                    idx_last_el = (excluded_paths[idx].split("/"))[-1]
                    path_last_el = path.split("/")[-1]
                    if path_last_el.startswith(idx_last_el[:-1]):
                        excluded_paths[idx] = path
                else:
                    continue
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
        request validation

        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if request is None or not request.headers.get("Authorization"):
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
