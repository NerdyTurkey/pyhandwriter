# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:28:38 2020

@author: jt
"""

# Pygame Colour Selector

# Use mouse to select one or more colours you want.
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
