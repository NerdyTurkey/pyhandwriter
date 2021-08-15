# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 18:43:05 2021

@author: jwgti
"""

import pygame as pg


def colorize(image, newColor):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()
    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pg.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pg.BLEND_RGBA_ADD)

    return image
