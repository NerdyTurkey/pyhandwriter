# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 12:59:13 2021

@author: jwgti
"""

from .style_tokens import STYLE_TOKENS
from .settings import ESC_CHARS

# following converts "\\bold" to "bold{" etc
STYLE_ESC_TOKENS = [token[1:] + "{" for token in STYLE_TOKENS.values()]

ALL_ESC_TOKENS = ESC_CHARS + STYLE_ESC_TOKENS


def get_illegal_index(s, tokens=ALL_ESC_TOKENS):
    """
    Returns index in 's' of first escaped token that in not in tokens.
    If no illegal token is found, returns None
    """
    backslash = "\\"  # this is a single backslash!
    i = 0  # char counter
    while i < len(s):
        c = s[i]
        if c != backslash:
            i += 1
            continue
        if c == backslash:
            if i + 1 < len(s) and s[i + 1] == " ":
                # ignoe backslash followed by space
                i += 2
                continue
            else:
                is_legal = False
                for token in tokens:
                    try:
                        ss = s[i + 1 : i + 1 + len(token)]
                    except IndexError:
                        continue
                    if ss == token:
                        is_legal = True
                        i += len(token)
                        break
                    else:
                        continue
                if not is_legal:
                    return i + 1
    return None
