# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 08:45:25 2021

@author: NerdyTurkey
"""

# For sorting strings containing numbers in natural order
# i.e. file1, file2, file10, file111
# rather than dumb sort which gives
# file1, file10 file11, file2

import re


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split(r"(\d+)", text)]
