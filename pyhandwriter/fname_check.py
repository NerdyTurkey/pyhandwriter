# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 08:33:40 2021

@author: jwgti
"""

# see wikipedia "filenames"
from . import settings as s

# add the fname separator to illegal chars
fname_sep = s.PROPS_GEN["fname_separator"]
ILLEGAL_CHARS = [
    ">",
    "<",
    ":",
    '"',
    "\\",
    "/",
    "|",
    "?",
    "*",
    "%",
    "=",
    ".",
    ";",
    "!",
    fname_sep,
]


def is_valid_fname(s):
    """
    Returns true if s is a valid windows filename.
    """
    if not s:
        return False
    if not isinstance(s, str):
        return False

    for c in s:
        if c in ILLEGAL_CHARS:
            return False
    return True
