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

DEFAULT_TEXT = "The quick brown fox jumps over the lazy dog"
HELP_TEXT = "LEFT/RIGHT ARROW FOR NEXT/PREVIOUS PAGE, CLICK TO SELECT, ESC OR CLOSE WINDOW TO FINISH"


def get_hw_font_names():
    font_path = os.path.join(os.path.dirname(__file__), s.PROPS_GEN["hw_font_folder"])
    hw_font_names = set()  # to prevent duplications
    for filename in os.listdir(font_path):
        hw_font_names.add(filename.split(s.PROPS_GEN["fname_separator"])[0])
    return list(hw_font_names)


def show_hw_fonts(
    screen,
    text=DEFAULT_TEXT,
    text_size=30,
    num_chars=len(DEFAULT_TEXT),
    bg_col=colours.col("BLUE"),
    text_col=colours.col("YELLOW"),
    x_pad=20,
    y_pad=50,
):
    """
     Displays all available hw fonts in alphabetical order on screen in
     rows and columns.

     Depending on 'screen' size and 'text_size', if there are too many fonts
     to show on one page, they will be displayed over several screens. You can
     mmove through these with the arrow keys.

     Esc or close window to quit.

     The font name is displayed in the window caption when the mouse cursor
     hovers over the font. One or more fonts can be selected by clicking on
     them. The names of the selected fonts are returned as a list when the
     user quits.

    'num_chars' determines how many chars of the font name will be displayed,
    useful in case the names are very long.

    'x_pad' and 'y_pad' are integers that give the number of pixels spacing
     between rows and columns

    """

    def get_hw_surf(text, text_size=None, hw_font_name=None, text_col=None):
        surf = pg.Surface((int(0.9 * screen.get_width()), text_size * 2), pg.SRCALPHA)
        text_rect = surf.get_rect()  # .inflate((-5,-5))
        hw = HandWriter(surf, hw_font=hw_font_name)
        hw.write_text(
            text,
            text_rect=text_rect,
            pt_size=text_size,
            colour=text_col,
            instantly=True,
            nib=(3, 45),
        )
        return surf

    def finish():
        screen.blit(save_screen, (0, 0))
        pg.display.flip()
        selected = []
        for patch_sprites in patch_sprites_pages:
            for patch in patch_sprites:
                if patch.selected:
                    selected.append(patch.label)
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
    hw_font_names = get_hw_font_names()
    hw_font_names.sort(key=natural_keys)
    # accumulate pages
    for font_name in hw_font_names:
        # print(font_name)
        text_surf = get_hw_surf(
            text[:num_chars],
            text_size=text_size,
            hw_font_name=font_name,
            text_col=text_col,
        )
        Patch(patch_sprites, text_surf, font_name, (x, y))
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
