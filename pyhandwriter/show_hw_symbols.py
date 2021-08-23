# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 12:21:45 2021

@author: NerdyTurkey
"""

import os
import pygame as pg
from . import text_utils as tu
from . import colours
from .natural_sort import natural_keys
from .patch import Patch
from .handwriter import HandWriter
from . import settings as s

HELP_TEXT = "LEFT/RIGHT ARROW FOR NEXT/PREVIOUS PAGE, CLICK TO SELECT, ESC OR CLOSE WINDOW TO FINISH"


def get_hw_symbol_names():
    font_path = os.path.join(os.path.dirname(__file__), s.PROPS_GEN["hw_symbol_folder"])
    hw_symbol_names = set()  # to prevent duplications
    for filename in os.listdir(font_path):
        name = filename.split(s.PROPS_GEN["fname_separator"])[1].split(".")[0]
        hw_symbol_names.add(name)
    return list(hw_symbol_names)


def show_hw_symbols(
    screen,
    text_size=60,
    bg_col=colours.col("BLUE"),
    text_col=colours.col("YELLOW"),
    x_pad=20,
    y_pad=60,
):

    """
    Displays all available hw symbols in alphabetical order on screen in
    rows and columns.

    Depending on 'screen' size and 'text_size', if there are too many symbols
    to show on one page, they will be displayed over several screens. You can
    mmove through these with the arrow keys.

    Esc or close window to quit.

    The symbols name is displayed in the window caption when the mouse cursor
    hovers over the symbol. One or more symbols can be selected by clicking on
    them. The names of the selected symbols are returned as a list when the
    user quits. The list is in selection order.

    'x_pad' and 'y_pad' are integers that give the number of pixels spacing
    between rows and columns

    """

    def get_hw_surf(text, text_size=None, text_col=None):
        surf = pg.Surface((int(text_size * 2), int(text_size * 2)), pg.SRCALPHA)
        text_rect = surf.get_rect()  # .inflate((-5,-5))
        # doesn't matter which hw_font is used, so default is fine
        hw = HandWriter(surf)
        hw.write_text(
            text,
            text_rect=text_rect,
            pt_size=text_size,
            colour=text_col,
            instantly=True,
            # nib=(3,45),
        )
        return surf

    def finish():
        screen.blit(save_screen, (0, 0))
        pg.display.flip()
        selected = []
        for patch_sprites in patch_sprites_pages:
            for patch in patch_sprites:
                if patch.selected:
                    selected.append((patch.label, patch.time_selected))
        # sort on selection time
        selected.sort(key=lambda x: x[1])
        # return just labels, not time selected
        return [s[0] for s in selected]
        return selected

    FPS = 60
    clock = pg.time.Clock()
    save_screen = screen.copy()
    dy = text_size + y_pad
    x0, y0 = 10, 10  # topleft start position
    x, y = x0, y0
    max_w = 0  # max text box width in current column
    w, h = screen.get_size()
    patch_sprites_pages = []
    patch_sprites = pg.sprite.Group()
    hw_symbol_names = get_hw_symbol_names()
    hw_symbol_names.sort(key=natural_keys)
    # accumulate pages
    for symbol_name in hw_symbol_names:
        # print(symbol_name)
        text_surf = get_hw_surf(
            text="`" + symbol_name + "`", text_size=text_size, text_col=text_col
        )
        Patch(patch_sprites, text_surf, symbol_name, (x, y))
        tw = text_surf.get_width()
        if tw > max_w:
            max_w = tw
        y += dy
        if y > h - dy:
            # new column
            y = y0
            x += max_w + x_pad
            if x > w - max_w:
                # new page
                patch_sprites_pages.append(patch_sprites)
                x, y = x0, y0
                patch_sprites = pg.sprite.Group()
                # page = blank_page.copy()
            max_w = 0
    patch_sprites_pages.append(patch_sprites)

    # display pages
    page_num = 0
    num_pages = len(patch_sprites_pages)

    while True:
        patch_sprites = patch_sprites_pages[page_num]
        clock.tick(FPS)
        clicked = False
        #   Check for user events
        events = pg.event.get()
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                clicked = True
            if e.type == pg.QUIT:
                return finish()
            if e.type == pg.KEYUP:
                if e.key == pg.K_ESCAPE:
                    return finish()
                elif e.key in [pg.K_UP, pg.K_LEFT]:
                    page_num -= 1
                elif e.key in [pg.K_DOWN, pg.K_RIGHT]:
                    # go to next page
                    page_num += 1
        # wrap-around pages
        if page_num < 0:
            page_num = num_pages - 1
        elif page_num > num_pages - 1:
            page_num = 0

        #   update
        patch_sprites.update(clicked)

        #   draw
        screen.fill(bg_col)
        tu.blit_text(
            HELP_TEXT,
            screen,
            text_handle="midbottom",
            surf_handle="midbottom",
            pt_size=14,
            col=colours.col("LIGHTGRAY"),
        )
        patch_sprites.draw(screen)
        pg.display.flip()
