# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 17:09:17 2020

@author: jt
"""

import pygame as pg
import pyhandwriter as ph

WIDTH = 900
HEIGHT = 600
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))

# Some cursors ------------------------------------------------------------

# ... circle
radius = 5
circle_cursor = pg.Surface((2 * radius, 2 * radius), pg.SRCALPHA)
pg.draw.circle(circle_cursor, ph.col("WHITE"), (radius, radius), radius, 1)
pg.image.save(circle_cursor, "assets/circle_cursor.png")

# ... crosshair
width = 10
crosshair_cursor = pg.Surface((width, width), pg.SRCALPHA)
pg.draw.line(crosshair_cursor, ph.col("WHITE"), (0, width // 2), (width, width // 2))
pg.draw.line(crosshair_cursor, ph.col("WHITE"), (width // 2, 0), (width // 2, width))
pg.image.save(crosshair_cursor, "assets/crosshair_cursor.png")

# ... square
width = 10
square_cursor = pg.Surface((width, width), pg.SRCALPHA)
pg.draw.rect(square_cursor, ph.col("WHITE"), square_cursor.get_rect(), 1)
pg.image.save(square_cursor, "assets/square_cursor.png")

# ... pencil
height = 50
pencil_cursor = pg.image.load("assets/pencil.png").convert_alpha()
w, h = pencil_cursor.get_size()
sf = height / h
pencil_cursor = pg.transform.scale(pencil_cursor, (int(w * sf), int(h * sf)))
pg.image.save(pencil_cursor, "assets/pencil_cursor.png")


# ... arrow
height = 20
arrow_cursor = pg.image.load("assets/arrow.png").convert_alpha()
w, h = arrow_cursor.get_size()
sf = height / h
arrow_cursor = pg.transform.scale(arrow_cursor, (int(w * sf), int(h * sf)))
pg.image.save(arrow_cursor, "assets/arrow_cursor.png")

pg.quit()
