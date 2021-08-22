# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:28:38 2020

@author: jt
"""

# demo2.py
# Recording a font & symbols using the Recorder class

import os
from pathlib import Path

path = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(path))
import pygame as pg
import pyhandwriter as ph

# screen dimensions
WIDTH, HEIGHT = 900, 600

pg.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("demo2.py")

# gigi was the font we liked previously, so use this as the prompt font
# to enable us to trace it; and we'll save our handwritten version to
# "my_gigi_"
recorder = ph.Recorder(screen)
recorder.record_font("my_gigi_", prompt_font="gigi")


# Let's also record some custom symbols.
# We'll record the Greek symbols alpha and beta, a heart shape and some music
# notes. We'll save them as "alpha", "beta", "heart" and "music" and then
# they will be available within any font we later want to handwrite with
# by embedding the name in back ticks (like markup).
recorder.record_symbols()


pg.quit()
