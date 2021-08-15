# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 08:49:54 2021

@author: jwgti
"""


def get_contrasting_col(col):
    """ Returns visually most contrasting colour """
    r, g, b = col[:3]  # ignore alpha channel here
    cr = 0 if r > 128 else 255
    cg = 0 if g > 128 else 255
    cb = 0 if b > 128 else 255
    return cr, cg, cb
