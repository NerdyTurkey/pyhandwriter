# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:28:38 2020

@author: jt
"""

# demo3.py
# Writing our recorded font using HandWriter class

import os
from pathlib import Path

path = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(path))
import pygame as pg
import pyhandwriter as ph


# screen dimensions
WIDTH = 1440
HEIGHT = 960


pg.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("demo3.py")


hw = ph.HandWriter(screen, hw_font="my_gigi")

# note use of built in \n and \t for newline and tab
text = (
    r"Hello youtube! \nThis is my_gigi font"
    r"\nand some symbols we defined"
    r"\n\t`alpha`\t`beta`\t`heart`\t`music`"
)

hw.write_text(text, pt_size=80, speed_mult=1.5, linewidth=3)

# Let's define the text area and jazz it up with some other options.
# To see al the options, type help(hw.write_text) in console
b = 100  # border
text_rect = pg.Rect(b, b, WIDTH - 2 * b, HEIGHT - 2 * b)
hw.write_text(
    text,
    pt_size=80,
    speed_mult=3,
    cursor="quill_dark",
    cursor_sf=2,
    nib={"width": 8, "angle": 45},
    colour=(8, 75, 131),
    text_rect=text_rect,
    surf_bg_col=(66, 191, 221),
    text_rect_bg_col=(187, 230, 228),
    text_rect_border_width=20,
    text_rect_border_col=(255, 102, 180),
)

# wait until keypressed or window closed
waiting = True
while waiting:
    for e in pg.event.get():
        if e.type in [pg.KEYDOWN, pg.QUIT]:
            waiting = False

pg.quit()
