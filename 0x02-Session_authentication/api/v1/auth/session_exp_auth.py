#!/usr/bin/env python3
"""session auth expiration module"""
from api.v1.auth.session_auth import SessionAuth

from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session auth class with expiration"""
    def __init__(self):
        """instance initialization"""
        try:
            SD = int(getenv('SESSION_DURATION'))
        except Exception:
            SD = 0
        self.session_duration = SD

    def create_session(self, user_id=None):
        """
        session creation

        Args:
            user_id (_type_, optional): _description_. Defaults to None.
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}

        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        get user by session id

        Args:
            session_id (_type_, optional): _description_. Defaults to None.
        """
        if session_id is None:
            return None

        user_details = self.user_id_by_session_id.get(session_id)

        if user_details is None:
            return None
        else:
            if user_details.get('created_at') is None:
                return None

            created_at = user_details.get('created_at')
            limit = created_at + timedelta(seconds=self.session_duration)

            if limit < datetime.now():
                return None
            else:
                return user_details.get('user_id')

            if self.session_duration <= 0:
                return user_details.get('user_id')
