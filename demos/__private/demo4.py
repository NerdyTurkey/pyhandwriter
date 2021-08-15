# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:28:38 2020

@author: jt
"""

# demo4.py
# Writing our recorded font using write_text() method: spray can cursor

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

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("demo3.py")

hw = ph.HandWriter(screen)  # go back to default font

text = r"Sorry about your wall `happy`"  # happy is built in symbol

hw.write_text(
    text,
    pt_size=200,
    speed_mult=1,
    cursor="spray_can",
    spray=dict(width=25, col=(255, 0, 255, 255), aspect_ratio=1, angle=0),
)

#  wait until keypressed or window closed
waiting = True
while waiting:
    for e in pg.event.get():
        if e.type == pg.KEYDOWN:
            waiting = False

        if e.type == pg.QUIT:
            waiting = False

pg.quit()
