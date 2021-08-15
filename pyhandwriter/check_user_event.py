# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 08:41:09 2020

@author: jt
"""

import pygame as pg
from enum import Enum, auto


class UserEvent(Enum):
    KEY_PRESSED = auto()
    WINDOW_CLOSED = auto()
    ESCAPED = auto()


def check_user_event():

    for e in pg.event.get():

        if e.type == pg.QUIT:
            return UserEvent.WINDOW_CLOSED

        elif e.type == pg.KEYDOWN:

            if e.key == pg.K_ESCAPE:
                return UserEvent.ESCAPED

            else:
                return UserEvent.KEY_PRESSED

    return None
