# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 06:23:49 2021

@author: NerdyTurkey
"""

from enum import Enum, auto


class Flag(Enum):
    FAIL = auto()
    FINISHED = auto()
    USER_QUIT = auto()
    OVERFLOW = auto()
