#!/usr/bin/env python3
"""session auth module"""
from api.v1.auth.auth import Auth
from models.user import User

from os import getenv
from uuid import uuid4


class SessionAuth(Auth):
    """session auth mechanism class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        instance method that creates session id for a user id

        Args:
            user_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        instance method that gets user id based on session id

        Args:
            session_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if session_id is None and not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        instance method that identifies a user via session id

        Args:
            request (_type_, optional): _description_. Defaults to None.
        """
        req_session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(req_session_cookie)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        instance method to destroy session id

        Args:
            request (_type_, optional): _description_. Defaults to None.
        """
        if request is None:
            return None

        session_id = self.session_cookie(request)

        if not session_id:
            return False
        else:
            if not self.user_id_for_session_id(session_id):
                return False
            else:
                del self.user_id_by_session_id[session_id]
                return True
