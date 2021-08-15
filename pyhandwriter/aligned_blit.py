# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:56:07 2021

@author: jwgti
"""

from sys import exit
import pygame as pg

vec = pg.math.Vector2


def aligned_blit(surf1, surf2, offset=None, handle1=None, handle2=None):
    """
    Blits surf1 to surf1 with 'handle1' (handle of surf1) displaced by 'offset'
    from 'handle2' (handle of surf2).

    A handle is a pygame rect descriptor in
    ("topleft", "midtop", "topright",
    "midright",
    "center"
    "bottomright", "midbottom", "bottomleft",
    "midleft")

    If None is passed for a handle, then that handle reverts to "topleft".

    offset is a (x_offset, y_offset) tuple that follows pygame axes convention
    i.e. x increasing from left to right & y increasing from top to bottom.
    e.g. offset=(20,-10) --> shift right by 20 pixels, shift up by 10 pixels

    returns text_rect (topleft relative to surf)

    Examples:
        aligned_blit(surf1, surf2)
            -> surf1 blitted onto surf2 with toplefts coinciding
        aligned_blit(surf1, surf2, offset=(50,50))
            -> surf1 blitted onto surf2 with surf1 topleft offset by (50,50) rel to surf2 topleft
        aligned_blit(surf1, surf2, handle1="center", handle2="center")
            -> surf1 blitted onto surf2 with centres coinciding
        aligned_blit(surf1, surf2, offset=(50,50), handle1="center")
            -> surf1 blitted onto surf2 with surf1 center offset by (50,50) rel to surf2 topleft
        aligned_blit(surf1, surf2, offset=(0,-100), handle1="center", handle2="midbottom")
            -> surf1 blitted onto surf2 with surf1 center offset by (0,-100) rel to surf2 midbottom
        aligned_blit(surf1, screen, offset=(-200,80), handle1="midright", handle2="topright")
            -> surf1 blitted onto surf2 with surf1 midright offset by (-200,80) rel to surf2 topright
    """
    handles = (
        "topleft",
        "midtop",
        "topright",
        "midright",
        "center",
        "bottomright",
        "midbottom",
        "bottomleft",
        "midleft",
    )
    if handle1 is not None and handle1.lower() in handles:
        handle1 = handle1.lower()
    else:
        handle1 = "topleft"
    if handle2 is not None and handle2.lower() in handles:
        handle2 = handle2.lower()
    else:
        handle2 = "topleft"
    offset = (0, 0) if offset is None else offset
    rect1 = surf1.get_rect()
    rect2 = surf2.get_rect()
    try:
        setattr(rect1, handle1, offset)
        rect1.topleft = vec(rect1.topleft) + vec(getattr(rect2, handle2))
        surf2.blit(surf1, rect1)
    except:
        print("Error!")
    return rect1


def main():
    # screen dimensions
    WIDTH = 900
    HEIGHT = 600
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    w, h = 100, 100
    surf1 = pg.Surface((w, h), pg.SRCALPHA)
    pg.draw.rect(surf1, (255, 255, 255), (0, 0, w, h), 1)
    # comment out all but one example
    # mod_rect = aligned_blit(surf1, screen)
    # mod_rect = aligned_blit(surf1, screen, offset=(50,50))
    # mod_rect = aligned_blit(surf1, screen, handle1="center", handle2="center")
    # mod_rect = aligned_blit(surf1, screen, offset=(50,50), handle1="center")
    # mod_rect = aligned_blit(surf1, screen, offset=(0,-100), handle1="center", handle2="midbottom")
    mod_rect = aligned_blit(
        surf1, screen, offset=(-200, 80), handle1="midright", handle2="topright"
    )
    # mod_rect = aligned_blit(surf1, screen, offset=10, handle1="midright", handle2="topright") #  should throw error
    pg.display.update(mod_rect)
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return
            elif e.type == pg.KEYUP:
                if e.key == pg.K_ESCAPE:
                    return


if __name__ == "__main__":
    main()
    pg.quit()
    exit()
