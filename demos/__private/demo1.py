# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:28:38 2020

@author: jt
"""

# demo1.py
# Choosing a font using the show_pygame_fonts() method

from pathlib import Path

path = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(path))

# The code above assumes the following directory structure
# project/
# |--- pyhandwriter/
# |--- demos/
#      |--- demo1.py
#      |--- demo2.py
#      |--- demo3.py
#      etc

import pygame as pg
import pyhandwriter as ph

# screen dimensions
WIDTH = 900
HEIGHT = 600

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("demo1.py")

selected_fonts = ph.show_pygame_fonts(screen)
print(selected_fonts)

pg.quit()
