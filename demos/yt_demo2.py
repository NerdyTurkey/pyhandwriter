# -*- coding: utf-8 -*-
"""

NerdyTurkey

"""
# demo2.py
# Recording a font & symbols using the Recorder class

import os
import sys

import pygame as pg

# Add the path to the project to the system path.
# In this example, the demos are in a sibling folder to the pyhandwriter project folder
from pathlib import Path

path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(path))
import pyhandwriter as ph


# screen dimensions
WIDTH, HEIGHT = 900, 600

pg.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("demo2.py")

recorder = ph.Recorder(screen)

recorder.record_symbols()

pg.quit()
