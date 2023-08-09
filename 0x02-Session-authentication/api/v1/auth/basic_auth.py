#!/usr/bin/env python3
"""basic auth module"""
from api.v1.auth.auth import Auth
from models.user import User
from models.base import Base, DATA
import base64
from typing import TypeVar


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
            idx = 0
            for i in range(len(decoded_base64_authorization_header)):
                if decoded_base64_authorization_header[i] == ':':
                    idx = i
                    break

            credentials = (
                decoded_base64_authorization_header[:idx],
                decoded_base64_authorization_header[idx+1:]
            )

            return credentials

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """
        user obj from credentials

        Args:
            self (_type_): _description_
        """
        if (
            user_email is None or
            not isinstance(user_email, str)
        ):
            return None

        if (
            user_pwd is None or
            not isinstance(user_pwd, str)
        ):
            return None

        User.load_from_file()

        if DATA['User']:
            res = None

            for _, userInstance in DATA['User'].items():
                if userInstance.search({"email": user_email}):
                    if userInstance.is_valid_password(user_pwd):
                        res = userInstance

            return res
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """_summary_"""
        authorization = self.authorization_header(request)
        auth_base64 = self.extract_base64_authorization_header(authorization)
        decoded_base64 = self.decode_base64_authorization_header(auth_base64)
        user_cred = self.extract_user_credentials(decoded_base64)
        user_obj = self.user_object_from_credentials(
            user_email=user_cred[0],
            user_pwd=user_cred[1]
        )

        return user_obj
