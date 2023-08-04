#!/usr/bin/env python3
"""script for handling the personal data
"""
import re
from typing import List
import logging
from os import environ
import mysql.connector


# PII fields
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """A function called filter_datum that returns the
        log message obfuscated:
    Arguments:
        1. fields: a list of strings representing all
        fields to obfuscate
        2. redaction: a string representing by what the
        field will be obfuscated
        3. message: a string representing the log line
        4. separator: a string representing by which character
        is separating all fields in the log line (message)
    The function should use a regex to replace occurrences of
    certain field values.
    filter_datum should be less than 5 lines long and use
    re.sub to perform the substitution with a single regex.
    """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """retuns logger objecte to handle the personal data

        retuns: Logging.logger
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns MySQLConnection object to access the personal dta

    Returns:
        A MySQLConnection object that extract detail saved
        on the environment.
    """
    username = environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    password = environ.get('PERSONAL_DATA_DB_PASSWORD', "")
    host = environ.get('PERSONAL_DATA_DB_HOST', "localhost")
    db_name = environ.get('PERSONAL_DATA_DB_NAME')

    connect = mysql.connector.connection.MySQLConnection(user=username,
                                                         password=password,
                                                         host=host,
                                                         database=db_name)
    return connect


def main():
    """
    Main function to retrieve user data from database and log to console
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT *FROM users;")
    field_name = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_name))
        logger.info(str_row.strip())
    
    cursor.close()
    db.close()

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Constructor method for RedactingFormatter class
        argument:
            fields: a list of strings representing all
                fields to obfuscate
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        reverts the log of a specified log int text.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ == '__main__':
    main()
