#!/usr/bin/env python3
"""session db authentication module"""
from datetime import datetime, timedelta

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session DB Auth class object"""

    def create_session(self, user_id=None):
        """create session id"""
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """get user id by session id"""
        try:
            session_list = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(session_list) <= 0:
            return None
        cur_time = datetime.now()
        created_at = session_list[0].created_at
        duration = timedelta(seconds=self.session_duration)
        limit = session_list[0].created_at + duration
        if limit < cur_time:
            return None
        return session_list[0].user_id

    def destroy_session(self, request=None):
        """destroy session id"""
        session_id = self.session_cookie(request)
        try:
            session_list = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(session_list) <= 0:
            return False
        session_list[0].remove()
        return True
