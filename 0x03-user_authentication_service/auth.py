#!/usr/bin/env python3
"""auth module"""
import bcrypt

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    returns the hashed byte version of password

    Args:
        password (str): _description_

    Returns:
        bytes: _description_
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register user by email and password

        Args:
            email (str): _description_
            password (str): _description_

        Returns:
            User: _description_
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
            else:
                hashed_pw = _hash_password(password)
                reg_user = self._db.add_user(email, hashed_pw)
                return reg_user
        except Exception as e:
            print(e)
