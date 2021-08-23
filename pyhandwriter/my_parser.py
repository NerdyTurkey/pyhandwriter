# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 18:18:49 2020

@author: NerdyTurkey
"""

def parse(string, tokens, open_brack=None, close_brack=None):
    open_brack = open_brack or "{"
    close_brack = close_brack or "}"

    styles = []
    parsed = []
    for i, c in enumerate(string):
        if c == open_brack:
            # check if chars preceding open_brack are a token_pattern
            found = False
            for token_key, token_pattern in tokens.items():
                if i - len(token_pattern) >= 0:
                    if string[i - len(token_pattern) : i] == token_pattern:
                        found = True
                        parsed = parsed[
                            : -len(token_pattern)
                        ]  # remove token pattern and '{'
                        styles.append(token_key)  # add the key to the current styles
                        break
            if not found:
                # this open_brack is just a regular text char
                parsed.append((set(styles), c))

        elif c == close_brack:  # and styles:
            if i > 0 and string[i - 1] != "\\":
                # this close_brack is a closing bracket for a style directive
                try:
                    styles.pop()
                except IndexError:
                    return None
            else:
                # this close_brack is just a regular char
                if i > 0:
                    # remove the '\\'
                    parsed.pop()

                parsed.append((set(styles), c))
        else:
            # just a regular char
            parsed.append((set(styles), c))

    return parsed
