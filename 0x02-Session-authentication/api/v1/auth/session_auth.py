#!/usr/bin/env python3
"""session auth module"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """session auth mechanism class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates session id for a user

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
