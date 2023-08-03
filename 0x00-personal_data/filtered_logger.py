#!/usr/bin/env python3
"""filtered logger module"""
import logging
from typing import List, Tuple
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
            '(?<={}=)[^{}]+'.format(field, separator),
            '{}'.format(redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format method for parent class

        Args:
            record (logging.LogRecord): _description_

        Returns:
            str: _description_
        """
        msg = super().format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
