#!/usr/bin/env python3
"""basic auth module"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """basic auth class"""
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """
        get encoded string from header

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

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """
        decode encoded string

        Args:
            base64_authorization_header (str): _description_

        Returns:
            str: _description_
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            res = base64.b64decode(base64_authorization_header)
            return res.decode("utf-8")
        except Exception as err:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        extract credentials

        Args:
            self (_type_): _description_
            str (_type_): _description_
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        else:
            credentials = tuple(decoded_base64_authorization_header.split(":"))
            return credentials
