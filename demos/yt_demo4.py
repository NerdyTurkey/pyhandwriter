# -*- coding: utf-8 -*-
"""

NerdyTurkey

"""

# demo4.py
# Writing our recorded font using HandWriter class: spray can cursor

import os
import sys

import pygame as pg

# Add the path to the project to the system path.
# In this example, the demos are in a sibling folder to the pyhandwriter project folder
from pathlib import Path

path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(path))
import pyhandwriter as ph

# screen dimensions
WIDTH, HEIGHT = 1440, 960


pg.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("demo4.py")

hw = ph.HandWriter(screen)  # go back to default font

text = r"Sorry about your wall `happy`"  # happy is built in symbol

hw.write_text(
    text,
    pt_size=200,
    speed_mult=0.75,
    cursor="spray_can",
    spray=dict(width=25, col=(255, 0, 255, 255), aspect_ratio=1, angle=0),
)

waiting = True
while waiting:
    for e in pg.event.get():
        if e.type in [pg.KEYDOWN, pg.QUIT]:
            waiting = False


pg.quit()
