#!/usr/bin/env python3
"""
password encryption module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    hash password by salting and encryption

    Args:
        password (str): _description_

    Returns:
        bytes: _description_
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
