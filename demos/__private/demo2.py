# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:28:38 2020

@author: jt
"""

# demo2.py
# Recording a font using the Recorder() method

from pathlib import Path

path = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(path))
import pygame as pg
import pyhandwriter as ph

# screen dimensions
WIDTH = 900
HEIGHT = 600


pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("demo2.py")

# gigi was the font we liked previously, so use this as the prompt font
# to enable us to trace it; and we'll save our handwritten version to
# "my_gigi_"
recorder = ph.Recorder(screen, "my_gigi_", prompt_font="gigi")
recorder.record()

pg.quit()
