#!/usr/bin/env python3
"""filtered logger module"""
import logging
from typing import List, Tuple, Union
import re


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: Union[List[str], Tuple[str], Tuple[str, ...]],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    function to filter user datum/data

    Args:
        fields (Union[List[str], Tuple[str]]):
            a list of fields to obfuscate
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

    def __init__(self, fields: Union[Tuple[str, ...], Tuple[str, ...]]):
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
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields, self.REDACTION,
            message, self.SEPARATOR
        )


def get_logger() -> logging.Logger:
    """returns logging.Logger object"""

    # creating logger object
    user_data_logger = logging.getLogger('user_data')
    user_data_logger.setLevel(logging.INFO)

    # creating stream handler to be logged on console
    stream_handler = logging.StreamHandler()

    # configuring a formatter
    formatter = logging.Formatter(RedactingFormatter(PII_FIELDS).FORMAT)

    # setting a formatter to the stream_handler
    stream_handler.setFormatter(formatter)

    # adding the streamhandler to the logger
    user_data_logger.addHandler(stream_handler)

    return user_data_logger
