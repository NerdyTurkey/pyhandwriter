ected_fonts# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:28:38 2020

@author: jt
"""

# Pygame Colour Selector - get names of pygame built in colours.

# All the common colours have obvious names, like "blue", "red" etc
# But there is a huge range of other colours with more cryptic names.

# These colour names can be used to colour your handwriting
# text = r"\colour_name{Hello world}"
# e.g. text = r"\aquarmarine3{Hello World}"
# e.g. text = r"\maroon1{Hello World}"

# Use the mouse to select one or more colours you want.
# When you quit (Esc or close window), the selected pygame colour names will be
# displayed in the order they were selected.

# For more info, type following at console
# help(ph.show_pygame_colours)

import sys
from pathlib import Path

path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(path))

import pygame as pg
import pyhandwriter as ph

# screen dimensions
WIDTH = 900
HEIGHT = 600

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Show colours demo")

selected = ph.show_pygame_colours(screen)

print(selected)

pg.quit()
sys.exit()
