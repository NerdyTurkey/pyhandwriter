# -*- coding: utf-8 -*-
"""

NerdyTurkey

"""

# demo1.py
# Choosing a font using the show_pygame_fonts() method

import os
import sys

import pygame as pg

# Add the path to the project to the system path.
# In this example, the demos are in a sibling folder to the pyhandwriter project folder
# project/
# |--- pyhandwriter/
# |--- demos/
#      |--- yt_demo1.py
#      |--- yt_demo2.py
#      |--- yt_demo3.py
#      etc
from pathlib import Path

path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(path))
import pyhandwriter as ph

# screen dimensions
WIDTH, HEIGHT = 900, 600

pg.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("demo1.py")

selected_fonts = ph.show_pygame_fonts(screen)
print(selected_fonts)

pg.quit()
