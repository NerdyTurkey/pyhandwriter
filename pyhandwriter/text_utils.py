# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 10:45:06 2020

@author: NerdyTurkey
"""
# For consistency, when using in other scripts
# import text_utils as tu
# line = tu.read_text_lines(filename)

import pygame as pg
import pygame.freetype
from .text_input import TextInput
from .aligned_blit import aligned_blit  # ToDo: move to gfx utils??

vec = pg.math.Vector2

# ==============================================================================


def read_text_lines(fname):
    # Using readlines()
    try:
        with open(fname, "r") as f:
            lines = f.readlines()

    except IOError:
        print("Error opening ", fname)
        return None

    # Strips the newline character
    processed_lines = []
    for line in lines:
        processed_lines.append(line.strip("\n"))

    return processed_lines


# ==============================================================================


def get_font(font_name, size=None):
    """
    Converts a font_name (string) to a pygame font object
    """

    if size is None:
        size = 18

    font_object = pg.freetype.SysFont("consolas", size)  # default value

    # First check if font_name is a system font
    if font_name in pg.freetype.get_fonts():
        return pg.freetype.SysFont(font_name, size)

    else:
        # Not a system font, so try loading it

        try:
            return pg.freetype.Font(font_name, size)

        except:
            # print('font not found - default will be substituted')
            pass

    return font_object


# ==============================================================================


def blit_text(
    text,
    surf,
    offset=None,
    text_handle=None,
    surf_handle=None,
    pt_size=None,
    font=None,
    col=None,
    bgnd_col=None,
    pad=None,
):
    """
    Blits text onto surf with text_handle offset by 'offset' from surf_handle.

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

    returns the text rect (topleft rel to surf topleft)
    """
    text_surf, _ = get_text_surface(
        text=text,
        text_size=pt_size,
        text_font_name=font,
        text_col=col,
        bgnd_col=bgnd_col,
        pad=pad,
    )
    text_rect = aligned_blit(
        text_surf, surf, offset=offset, handle1=text_handle, handle2=surf_handle
    )
    return text_rect


# ==============================================================================


def get_text_surface(
    text=None,
    text_size=None,
    text_font_name=None,
    text_col=None,
    bgnd_col=None,
    pad=None,
    show_origin=False,
):
    """
    Returns tuple:
        surf, (ox,oy)
    where surf is pygame surface with text rendered on it using the newer freetype module of pygame.
    (ox, oy) is the text 'origin' coords rel to topleft of surface,


    Note: the text origin is a reference point for vertical and horizontal alignment of the text
    e.g. if  you tried to align two such surface by their toplefts, an f would be too high compared to an a
    so need to ensure their origin positions align vertically etc.


    text_font_name is either the filename of a true type font or the name of a system font
    the function tries it as a file name first and if that fails it tries it as a
    system font, if that fails it uses the preloaded default true type font.

    The background_colour is transparent which is the default when
    bgcolor=None is passed to font.render().

    Note: the bounding box of the returned surface is tight around the text,
    ie. the minimum size it can be without clipping the text.

    """
    # default text properties
    DTP = {
        "text": "Some text",
        "text_size": 24,
        "text_font_name": "consolas",  # put your preferred default font name (or true type filename) here
        "text_col": (255, 255, 255),
    }
    text = text or DTP["text"]
    text_size = text_size or DTP["text_size"]
    text_col = text_col or DTP["text_col"]
    text_font_name = text_font_name or DTP["text_font_name"]
    pad = pad or 5
    font = get_font(text_font_name, text_size)
    # the topleft of rect returned by font.render is the text 'origin'
    text_surface, rect = font.render(
        text=text, fgcolor=text_col, bgcolor=bgnd_col
    )  # bgnd_col=None --> transparent bgnd
    ox, oy = rect.topleft
    if show_origin:
        pg.draw.circle(
            text_surface, (255, 0, 0), (rect[0], rect[1]), 5
        )  # debug to see where origin is
    if pad:
        w, h = text_surface.get_size()
        padded_text_surface = pg.Surface((w + 2 * pad, h + 2 * pad), pg.SRCALPHA)
        if bgnd_col is not None:
            padded_text_surface.fill(bgnd_col)
        padded_text_surface.blit(text_surface, (pad, pad))
        return padded_text_surface.convert_alpha(), (ox + pad, oy + pad)
    else:
        return text_surface.convert_alpha(), (ox, oy)


# ==============================================================================


def match(lst=None, string=None, case_sensitive=True):
    """
    Returns True if any item in list is is contained in string.

    """
    if lst is None or string is None:
        return False

    for item in lst:
        if case_sensitive and item in string:
            return True
        if not case_sensitive and item.lower() in string.lower():
            return True
    return False


# ==============================================================================


def get_text_input(
    screen,
    font=None,
    text_size=16,
    max_len=20,
    text_color=(0, 0, 255),
    topleft=(100, 100),
):
    """
    Read in text typed by user.
    Wrapper for TextInput module.
    """
    clock = pg.time.Clock()
    textinput = TextInput(
        font_name=font,
        text_size=text_size,
        text_color=text_color,
        max_string_length=max_len,
    )
    save_screen = screen.copy()
    while True:
        screen.blit(save_screen, (0, 0))
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                return None
        # Feed it with events every frame
        ret_val = textinput.update(events)
        # only way to finish it to press return
        if ret_val:
            screen.blit(save_screen, (0, 0))  # restore screen
            return textinput.get_text()  # return entered text
        # Blit its surface onto the screen
        screen.blit(textinput.get_surface(), topleft)
        pg.display.flip()
        clock.tick(30)


# ==============================================================================


def get_text_size(font_name=None, size=None, max_len=None):
    """
    Return(width, height) of bounding text box for max_len characters of font_name
    with point size 'size'.
    An 'M' is used to provide the max possible width for variable width fonts.
    """
    font = get_font(font_name, size=size)

    return font.get_rect("M" * max_len, size=size).size  # 'M' is wide character
