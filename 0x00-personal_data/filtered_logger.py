#!/usr/bin/env python3
"""filtered logger module"""
from typing import List
import re


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    function to filter user datum/data

    Args:
        fields (List[str]): a list of fields to obfuscate
        redaction (str): obfuscating string
        message (str): the log line
        separator (str): the character separating all fields in
            the message

    Returns:
        str: string with obfuscated fields
    """
    for field in fields:
        message = re.sub(
            r'(?<={}=)[^{}]+'.format(field, separator),
            '{}={}'.format(field, redaction), message)
    return message
