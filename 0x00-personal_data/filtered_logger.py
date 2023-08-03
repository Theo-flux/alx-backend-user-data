#!/usr/bin/env python3
"""filtered logger module"""
from os import environ
import logging
from typing import List, Tuple, Union
import re
import mysql.connector


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
            r'(?<={}=)[^{}]+'.format(field, separator),
            '{}={}'.format(field, redaction), message)
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

    # setting logger level
    user_data_logger.setLevel(logging.INFO)

    # preventing propagation to parent logger
    user_data_logger.propagate = False

    # creating stream handler to be logged on console
    stream_handler = logging.StreamHandler()

    # configuring a formatter
    formatter = logging.Formatter(RedactingFormatter(PII_FIELDS).FORMAT)

    # setting a formatter to the stream_handler
    stream_handler.setFormatter(formatter)

    # adding the streamhandler to the logger
    user_data_logger.addHandler(stream_handler)

    return user_data_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """starts a db connection"""
    user = environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    database = environ.get('PERSONAL_DATA_DB_DATABASE', 'holberton')

    return mysql.connector.connection.MySQLConnection(
        user=user,
        password=password,
        host=host,
        database=database
    )


def main() -> None:
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')

    logger = get_logger()
    fields = cursor.column_names

    for row in cursor:
        row = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(row.strip())
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
