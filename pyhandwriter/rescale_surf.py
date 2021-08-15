# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 13:17:11 2020

@author: jt
"""


import pygame as pg


def rescale_surf(surf, width=None, height=None):
    """
    Rescales a pygame surface ensuring aspect ratio is maintained.

    width and height are in screen pixels.

    If one of width or height is passed, the returned surf width or height
    is set to this value.

    If both are passed, the final size is the smallest one closest to the
    requested sizes, while maintaing the aspect ratio.

    If neither width nor height is passed, the original image is returned
    """

    if width is None and height is None:
        return surf

    w, h = surf.get_size()

    if width is not None and height is None:
        sf = width / w

    elif height is not None and width is None:
        sf = height / h

    else:
        # both are not None
        sf = min(width / w, height / h)

    return pg.transform.rotozoom(surf, 0, sf)
