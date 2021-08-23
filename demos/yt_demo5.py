# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 11:35:07 2021

@author: jt
"""
# demo5.py
# Writing a secret message

import os
import pickle
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
pg.display.set_caption("demo5.py")

with open("secret_msg.pckl", "rb") as f:
    secret_msg = pickle.load(f)
    secret_font = pickle.load(f)

hw = ph.HandWriter(screen, hw_font=secret_font)

hw.write_text(secret_msg, pt_size=150, speed_mult=1.5, linewidth=3, char_spacing=3)


# wait until keypressed or window closed
waiting = True
while waiting:
    for e in pg.event.get():
        if e.type in [pg.KEYDOWN, pg.QUIT]:
            waiting = False

pg.quit()
