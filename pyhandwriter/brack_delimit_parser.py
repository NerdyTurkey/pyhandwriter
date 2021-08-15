# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 15:21:45 2020

@author: jt
"""


def bracket_parse(string, open_brack=None, close_brack=None, repl_string=None):
    """
    Returns: tuple parsed, mod_string
    where
    parsed is a list of text_snippets
    where text_snippet is text between open_brack and close_brack chars

    mod_string is string with each occurence of
    open_brack + text in between + close_brack
    replaced by repl_string

    Warning: does not work with nested brackets!!
    """
    open_brack = open_brack or "["
    close_brack = close_brack or "]"

    parsed = []
    adding = False
    text = ""
    mod_string = ""

    for c in string:
        if not adding:
            mod_string += c
        if c == open_brack:
            adding = True
            if repl_string is not None:
                mod_string = mod_string[:-1]
                mod_string += repl_string
        elif c == close_brack:
            parsed.append(text[1:])  # remove first char from text which will be
            text = ""
            adding = False
        if adding:
            text += c

    return parsed, mod_string


def delimiter_parse(string, delimiter="$", repl_string=""):
    """
    Returns: tuple: parsed, mod_string
    where
    parsed is a list of text_snippets
    where text_snippet is text between delimiter

    mod_string is string with each occurence of
    delimiter + text in between + delimter
    replaced by repl_string

    Warning: does not work with nested delimiters

    """

    string_split_at_delimiter = string.split(delimiter)
    # print('\nString split at delimiter = ', string_split_at_delimiter) # debug

    # NB: if string starts with delimiter,
    # then string_split_at_delimiter[0] == ''

    if len(string_split_at_delimiter) == 1:
        # no splits made --> no delimiters found
        return None, string

    inside_strings = string_split_at_delimiter[1::2]  # within delimiters

    if not string_split_at_delimiter[0]:
        # first element in split list is '' --> string started with delimiter
        outside_strings = string_split_at_delimiter[2::2]  # outside delimiters
    else:
        outside_strings = string_split_at_delimiter[0::2]  # outside delimiters

    # print('\nOutside strings = ', outside_strings) # debug

    rejoined_outside_strings = "".join([s + repl_string for s in outside_strings])
    # but this adds a replacement string at very end which we need to remove
    rejoined_outside_strings = rejoined_outside_strings[: -len(repl_string)]
    if not string_split_at_delimiter[0]:
        rejoined_outside_strings = repl_string + rejoined_outside_strings

    return inside_strings, rejoined_outside_strings


def main():
    # some examples

    # string ='[some crap] abcdefghijklm [some more crap] 1234567890 [last crap] ABCDEFGH'
    # print('\nInitial string = ', string)
    # print('bracket parsed =', bracket_parse(string, repl_string="ZYXW"))

    # string ='$$some crap$$ abcdefghijklm $$some more crap$$ 1234567890 $$last crap$$ ABCDEFGH'
    # print('\nInitial string = ', string)
    # print('delimiter parsed =', delimiter_parse(string, delimiter='$$',repl_string="ZYXW"))

    # string = 'This text contains no delimiters'
    # print('\nInitial string = ', string)
    # print('delimiter parsed =', delimiter_parse(string, delimiter='$$',repl_string="ZYXW"))

    # string = r'$inside0$First line of text $\frac{\cos(x)}{y^2+\exp(\pi)}$ some other text $y = a x^2 + b x + c$ goodbye.'

    string = (
        r"Here is an inline equation $x^2 -3$\n"
        r"and here is a newline equation £x=\frac{-b\pm\sqrt{b^2-4 a c}}{2 a}£"
        r"where $a$, $b$, $c$ are coefficients of quadrtic equation."
    )

    # string = r'First line of text $\frac{\cos(x)}{y^2+\exp(\pi)}$ some other text $y = a x^2 + b x + c$ goodbye.'
    print("\nInitial string = ", string)
    parsed, rejoined = delimiter_parse(string, delimiter="$", repl_string="\\$")
    print("\nParsed = ", parsed)
    print("\nRejoined = ", rejoined)

    string = rejoined
    # string = r'First line of text $\frac{\cos(x)}{y^2+\exp(\pi)}$ some other text $y = a x^2 + b x + c$ goodbye.'
    print("\nInitial string = ", string)
    parsed, rejoined = delimiter_parse(string, delimiter="£", repl_string="\\£")
    print("\nParsed = ", parsed)
    print("\nRejoined = ", rejoined)


if __name__ == "__main__":
    main()
