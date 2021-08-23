# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 17:14:45 2021

@author: NerdyTurkey
"""
from bisect import bisect_left


def get_closest(alist, val):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    alist.sort()
    pos = bisect_left(alist, val)
    if pos == 0:
        return alist[0]
    if pos == len(alist):
        return alist[-1]
    before = alist[pos - 1]
    after = alist[pos]
    if after - val < val - before:
        return after
    else:
        return before
