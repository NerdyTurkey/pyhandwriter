# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 21:30:15 2021

@author: NerdyTurkey
"""

import math
import pygame as pg
import colorsys
from . import colours
from .natural_sort import natural_keys
from .patch import Patch

vec = pg.math.Vector2


def get_patch_info(screen_size, num_patches):
    w, h = screen_size
    nc = math.ceil(math.sqrt(w * num_patches / h))  # num cols
    nr = math.ceil(num_patches / nc)  # num rows
    return nc, nr


def show_pygame_colours(screen, rainbow=True):
    """
    Shows all the named pygame colours (THECOLOURS) in a grid on a single
    screen.

    If rainbow, colours in an attempt at rainbow order starting from topleft
    and going row by row from left to right.

    If not rainbow, the ordering is alphabetical.

    The colour name is displayed in the window caption when the mouse cursor
    hovers over the colour. One or more colours can be selected by clicking on
    them. The names of the selected colours are returned as a list when the
    user quits (Esc or close window). The list is in the selection order.
    """

    def finish():
        screen.blit(save_screen, (0, 0))
        pg.display.flip()
        selected = []
        for patch in patch_sprites:
            if patch.selected:
                selected.append((patch.label, patch.time_selected))
        # sort on selection time
        selected.sort(key=lambda x: x[1])
        # return just labels, not time selected
        return [s[0] for s in selected]

    FPS = 60
    w, h = screen.get_size()
    clock = pg.time.Clock()
    save_screen = screen.copy()
    patch_sprites = pg.sprite.Group()
    col_list = [(col_name, col) for col_name, col in colours.col_dict.items()]

    if rainbow:
        # sort colours into "spectrum"; a few options to try
        # col_list.sort() # naive rgb sort
        col_list.sort(
            key=lambda el: colorsys.rgb_to_hsv(*el[1][:3])
        )  # hsv sort - I think this is best
        # col_list.sort(key=lambda el: step(el[1], 8)) # step sort
        # col_list.sort(key=lambda el: step2(el[1], 8)) # step2 sort
    else:
        # alphabetic
        col_list.sort(key=lambda el: natural_keys(el[0]))

    # spawn patch sprites
    num_colours = len(col_list)
    num_cols, num_rows = get_patch_info((w, h), num_colours)
    pw, ph = int(w / num_cols), int(h / num_rows)
    row_num = 0
    col_num = 0
    for i, (col_name, col) in enumerate(col_list):
        img = pg.Surface((pw, ph), pg.SRCALPHA)
        img.fill(col)
        Patch(patch_sprites, img, col_name, (col_num * pw, row_num * ph))
        col_num += 1
        if col_num == num_cols:
            col_num = 0
            row_num += 1

    # fill any unused screen area with black patches
    for row in range(row_num, num_rows):
        for col in range(col_num, num_cols):
            img = pg.Surface((pw, ph), pg.SRCALPHA)
            img.fill(colours.col("black"))
            Patch(patch_sprites, img, "black", (col * pw, row * ph))

    while True:
        clicked = False
        clock.tick(FPS)
        #   Check for user events
        events = pg.event.get()
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                clicked = True
            if e.type == pg.QUIT:
                return finish()
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    return finish()

        #   update
        patch_sprites.update(clicked)

        #   draw
        screen.fill(colours.col("black"))
        patch_sprites.draw(screen)
        pg.display.flip()
