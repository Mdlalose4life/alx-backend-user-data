#!/usr/bin/env python3
"""
script for handling the personal data
"""
import re
from typing import List
import logging

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