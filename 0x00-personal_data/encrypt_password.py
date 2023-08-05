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
    """
    check password validty with hashed value

    Args:
        hashed_password (bytes): _description_
        password (str): _description_

    Returns:
        bool: _description_
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
