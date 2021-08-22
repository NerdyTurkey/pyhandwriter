# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 11:38:42 2021

@author: jwgti
"""
import os
import pygame as pg

vec = pg.math.Vector2


def line_blit(surf, p1, p2, img, mult=1):
    """
    Draws a line on surf between points p1 and p2
    by blitting multiple copies of img between points.
    The images will be spaced to slightly overlap.
    The mult optinal argument can be used to increase or decrease
    the spacing, e.g. mult=2 --> twice as many images will be bitted.

    Parameters
    ----------
    surf: pygame surface, eg. screen
        surface on which to draw line
    p1 : tuple (int, int) or pygame vector2d
        start position
    p2 : tuple (int, int) or pygame vector2d
        end position
    img : pygame surface
        to blit mutliple times to make surface
        nb: line runs through centre of images
    mult : float
        A multipler that multiplies the number of images blitted

    Returns
    -------
    the rect bounding the changed pixels on the surface

    """
    fudge_factor = 5
    p1 = vec(p1)
    p2 = vec(p2)
    w, h = img.get_size()
    mid_pt = vec(w, h) / 2
    mean_size = (w + h) / 2
    line_vector = p2 - p1
    length = line_vector.length()
    if length == 0:
        # print("zero length line!")
        return
    unit_vector = line_vector / length
    num_blits = 1 + int(mult * fudge_factor * length / mean_size)
    delta = length / num_blits
    current_pos = vec(p1)
    blitted_rects = []  # list of blitted rects
    for _ in range(num_blits):
        blitted_rect = surf.blit(img, current_pos - mid_pt)
        blitted_rects.append(blitted_rect)
        current_pos += delta * unit_vector

    # ToDo might be a gap at p2??
    return blitted_rects[0].unionall(blitted_rects[1:])


def main():
    WIDTH, HEIGHT = 900, 600
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    path = os.path.join(os.path.dirname(__file__), "assets")
    spray_fname = os.path.join(path, "spray_softer.png")
    spray_img = pg.image.load(spray_fname).convert_alpha()
    modified_rect = line_blit(screen, (200, 200), (500, 500), spray_img)
    print(modified_rect)
    pg.display.update(modified_rect)

    while True:
        for e in pg.event.get():
            if e.type == pg.KEYDOWN or e.type == pg.QUIT:
                return


if __name__ == "__main__":
    main()
    pg.quit()
