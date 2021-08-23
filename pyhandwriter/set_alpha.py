# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 12:10:34 2021

@author: NerdyTurkey
"""

import pygame as pg


def set_alpha(image, alpha):
    tmp = pg.Surface(image.get_size(), pg.SRCALPHA)
    tmp.fill((255, 255, 255, alpha))
    img = image.copy()
    img.blit(tmp, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
    return img
