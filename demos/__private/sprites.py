# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 21:30:15 2021

@author: jwgti
"""
import pygame as pg
from random import randrange
from math import sin, cos, radians

vec = pg.math.Vector2


class Player(pg.sprite.DirtySprite):
    def __init__(self, sprite_group, layer, screen_size, img, pos=None, speed=None):
        self._layer = layer  # Note: need to set layer before super init!
        pg.sprite.DirtySprite.__init__(self)
        sprite_group.add(self)
        self.screen_width, self.screen_height = screen_size
        self.image = img
        self.pos = (
            vec(self.screen_width // 2, self.screen_height - 50)
            if pos is None
            else vec(pos)
        )
        self.rect = self.image.get_rect(midbottom=self.pos)
        self.width, self.height = self.rect.size
        speed = 1 if speed is None else speed
        self.vel = speed * vec(1, 0)  # horiz motion only for this demo

    def update(self, dt):
        keys = pg.key.get_pressed()
        delta_pos = dt * self.vel
        if keys[pg.K_RIGHT]:
            self.pos += delta_pos
        elif keys[pg.K_LEFT]:
            self.pos -= delta_pos
        x, y = int(self.pos.x), int(self.pos.y)
        if x + self.width // 2 > self.screen_width:
            self.pos -= delta_pos
        elif x - self.width // 2 < 0:
            self.pos += delta_pos
        self.rect.midbottom = x, y
        self.dirty = 1


class Rain(pg.sprite.DirtySprite):
    def __init__(
        self,
        sprite_group,
        layer,
        screen_size,
        col=None,
        length=None,
        angle=0,
        thickness=None,
        speed=None,
    ):
        self._layer = layer  # Note: need to set layer before super init!
        pg.sprite.DirtySprite.__init__(self)
        sprite_group.add(self)
        self.screen_width, self.screen_height = screen_size
        col = (45, 45, 45) if col is None else col
        length = 40 if length is None else int(length)
        length = length + randrange(length // 2, length)
        self.angle = 0 if angle is None else angle
        thickness = 1 if thickness is None else int(thickness)
        w = thickness + int(length * abs(sin(radians(self.angle))))
        h = int(length * cos(radians(self.angle)))
        self.image = pg.Surface((w, h), pg.SRCALPHA)
        self.pos = vec(randrange(self.screen_width), -randrange(self.screen_height))
        if self.angle >= 0:
            # sloping from topleft to bottom right
            self.rect = self.image.get_rect()
            p1 = self.rect.topleft
            p2 = self.rect.bottomright
            self.rect.topleft = self.pos
        else:
            # sloping from top right to bottom left
            self.rect = self.image.get_rect()
            p1 = self.rect.topright
            p2 = self.rect.bottomleft
            self.rect.topright = self.pos
        pg.draw.line(self.image, col, p1, p2, thickness)
        speed = 0.75 if speed is None else speed
        self.dirn = vec(0, 1).rotate(-self.angle)
        self.vel = speed * self.dirn

    def update(self, dt):
        self.pos += self.vel * dt
        # screen wrap
        x, y = int(self.pos.x % self.screen_width), int(self.pos.y % self.screen_height)
        if self.angle >= 0:
            self.rect.topleft = x, y
        else:
            self.rect.topright = x, y

        self.pos = x, y
        self.dirty = 1
