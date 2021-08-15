# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:28:38 2020

@author: jt
"""

# demo3.py
# Writing our recorded font using write_text() method

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

hw = ph.HandWriter(screen, hw_font="my_gigi_")

text = (
    r"Hello youtube! \nThis is my_gigi font"
    r"\nand some symbols we defined"
    r"\n\t`alpha`\t`beta`\t`heart`\t`music`"
)

hw.write_text(text, pt_size=80, speed_mult=1.5, cursor="pencil")

# wait until keypressed or window closed
waiting = True
while waiting:
    for e in pg.event.get():
        if e.type == pg.KEYDOWN:
            waiting = False

        if e.type == pg.QUIT:
            waiting = False

pg.quit()
