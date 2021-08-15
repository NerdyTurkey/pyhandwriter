# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:28:38 2020

@author: jt
"""

# Pygame Font Selector

# Use mouse to select one or more fonts you want.
# When you quit (Esc or close window), the selected pygame font names will be
#  displayed in the order they were selected.

# Further inturctions at bottom of pygame screen

# For more info, type following at console
# help(ph.show_pygame_fonts)

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
pg.display.set_caption("Show fonts & symbols demo")

# 1. Using default text
# selected = ph.show_pygame_fonts(screen)

# 2. Customise the displayed text for each font
# selected = ph.show_hw_fonts(screen, text="Hellow world 123")

# 3. Show symbols (built-ins and user recorded)
selected = ph.show_hw_symbols(screen)

print(selected)

pg.quit()
sys.exit()
