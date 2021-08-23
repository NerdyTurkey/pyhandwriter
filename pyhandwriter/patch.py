# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 11:39:34 2021

@author: NerdyTurkey
"""

import time
import pygame as pg

from .contrast import get_contrasting_col


class Patch(pg.sprite.DirtySprite):
    def __init__(self, sprite_group, img, label, pos):
        pg.sprite.Sprite.__init__(self)
        sprite_group.add(self)
        self.label = label
        self.image0 = img
        self.image = self.image0.copy()
        self.rect = self.image.get_rect(topleft=pos)
        self.image_hover = self.image0.copy()
        self.image_selected = self.image0.copy()
        contrast_col = get_contrasting_col(img.get_at((0, 0)))  # ToDo sample more pts
        pg.draw.rect(self.image_hover, contrast_col, self.image_hover.get_rect(), 8)
        pg.draw.rect(
            self.image_selected, contrast_col, self.image_selected.get_rect(), 4
        )
        self.selected = False

    def update(self, clicked):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            # hovered over
            pg.display.set_caption(self.label)
            self.image = self.image_hover.copy()
            # if pg.mouse.get_pressed()[0]:
            if clicked:
                self.selected = not self.selected
                if self.selected:
                    self.time_selected = time.time()
            return

        if self.selected:
            self.image = self.image_selected.copy()
        else:
            self.image = self.image0.copy()
