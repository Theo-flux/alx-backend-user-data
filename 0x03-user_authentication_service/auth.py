#!/usr/bin/env python3
"""auth module"""
import bcrypt
from uuid import uuid4

from sqlalchemy.orm.exc import NoResultFound
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


def _generate_uuid() -> str:
    """
    function that generates string
    representation of uuid
    """
    return str(uuid4())


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
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pw = _hash_password(password)
            user = self._db.add_user(email, hashed_pw)
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        check that credentials are for a valid user

        Args:
            email (str): _description_
            password (str): _description_

        Returns:
            bool: _description_
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        else:
            hashed_pwd = getattr(user, "hashed_password").decode('utf-8')
            if bcrypt.checkpw(
                password.encode('utf-8'),
                hashed_pwd.encode('utf-8')
            ):
                return True
            return False
