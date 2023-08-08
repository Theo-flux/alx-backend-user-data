#!/usr/bin/env python3
"""basic auth module"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """basic auth class"""
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """
        basic_auth server side

        Args:
            authorization_header (str): _description_

        Returns:
            str: _description_
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header[6:]
