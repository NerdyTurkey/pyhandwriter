# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 12:41:55 2020

@author: jt
"""

import pygame as pg


def convert_image_to_surface(img):
    """ converts img (eg. from PIL) to pygame surface """
    mode = img.mode
    size = img.size
    data = img.tobytes()
    return pg.image.fromstring(data, size, mode)
