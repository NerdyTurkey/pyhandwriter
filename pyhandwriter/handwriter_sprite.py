# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 21:34:30 2021

@author: NerdyTurkey
"""

import time  # more accurate than pygame timers

import pygame as pg

from .enums import Flag
from .handwriter_gen import HandWriterGen


class HandWriterSprite(pg.sprite.DirtySprite):
    """
    TODO docstring
    """
    # stores all instances to allow separate update call
    handwriter_sprites = pg.sprite.LayeredDirty()

    is_first_tick = True

    def __init__(
        self,
        sprite_group,
        layer,
        surf,
        text,
        surf_topleft=None,
        text_rect=None,
        hw_font=None,
        colour=None,
        linewidth=None,
        smooth_level=None,
        nib=None,
        spray=None,
        pt_size=None,
        char_spacing=None,
        word_spacing=None,
        line_spacing=None,
        speed_mult=None,
        instantly=False,
        cursor=None,
        cursor_sf=None,
        num_tabs=None,
        hyphenation=False,
        surf_bg_col=None,
        surf_border_width=None,
        surf_border_col=None,
        text_rect_bg_col=None,
        text_rect_border_width=None,
        text_rect_border_col=None,
    ):
        self._layer = layer  # Note: need to set layer before super init!
        pg.sprite.DirtySprite.__init__(self)
        self.sprite_group = sprite_group
        sprite_group.add(self)
        HandWriterSprite.handwriter_sprites.add(self)  # class var
        self.surf = surf
        self.text = text
        self.text_rect = text_rect
        self.hw_font = hw_font
        self.colour = colour
        self.linewidth = linewidth
        self.smooth_level = smooth_level
        self.nib = nib
        self.spray = spray
        self.pt_size = pt_size
        self.char_spacing = char_spacing
        self.word_spacing = word_spacing
        self.line_spacing = line_spacing
        self.speed_mult = speed_mult
        self.instantly = instantly
        self.cursor = cursor
        self.cursor_sf = cursor_sf
        self.num_tabs = num_tabs
        self.hyphenation = hyphenation
        self.surf_bg_col = surf_bg_col
        self.surf_border_width = surf_border_width
        self.surf_border_col = surf_border_col
        self.text_rect_bg_col = text_rect_bg_col
        self.text_rect_border_width = text_rect_border_width
        self.text_rect_border_col = text_rect_border_col
        self.image = surf
        self.surf_topleft = (20, 20) if surf_topleft is None else surf_topleft
        self.rect = self.image.get_rect(topleft=self.surf_topleft)
        self.orig_img = self.image.copy()
        self.finished = False
        self.quit_attempt = False
        self.overflow = False
        self.paused = False
        self.hw = HandWriterGen(self.surf, self.hw_font)
        self._set_generator()
        # self.is_first_tick = True

    def _set_generator(self):
        self.g = self.hw.write_text(
            self.text,
            update_display=False,  # a sprite surface won't be screen
            text_rect=self.text_rect,
            colour=self.colour,
            linewidth=self.linewidth,
            smooth_level=self.smooth_level,
            nib=self.nib,
            spray=self.spray,
            pt_size=self.pt_size,
            char_spacing=self.char_spacing,
            word_spacing=self.word_spacing,
            line_spacing=self.line_spacing,
            speed_mult=self.speed_mult,
            instantly=self.instantly,
            cursor=self.cursor,
            cursor_sf=self.cursor_sf,
            num_tabs=self.num_tabs,
            hyphenation=self.hyphenation,
            surf_bg_col=self.surf_bg_col,
            surf_border_width=self.surf_border_width,
            surf_border_col=self.surf_border_col,
            text_rect_bg_col=self.text_rect_bg_col,
            text_rect_border_width=self.text_rect_border_width,
            text_rect_border_col=self.text_rect_border_col,
        )  # generator

    def update(self, dt):
        # dt not used
        # In all cases, want sprite rect to continue to be updated in display
        # by setting self.dirty=1, else any other sprite passing over it will
        # leave trails; also sprite won't move properly.
        self.dirty = 1
        if self.finished or self.paused:
            # print(self, "in update, paused") # debug
            return
        try:
            val = next(self.g)
        except StopIteration:
            self.finished = True
        else:
            if val is Flag.USER_QUIT:
                self.quit_attempt = True
            elif val is Flag.OVERFLOW:
                self.overlow = True

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def reset(self):
        self.image = self.orig_img.copy()
        self.hw.change_surf(self.image)
        self.finished = False
        self.quit_attempt = False
        self.overflow = False
        self.paused = False
        self._set_generator()

    def change_text(self, text):
        self.reset()
        self.hw.change_text(text)

    def change_speed(self, sf):
        # generator needs to be started before sending something to it
        # so do one 'next' first
        try:
            next(self.g)
        except StopIteration:
            return
        self.g.send(sf)

    def hide(self):
        self.kill()

    def unhide(self):
        self.sprite_group.add(self)

    @classmethod
    def tick(cls, fps):
        now = time.time()
        elapsed_time_since_last_call_sec = 0
        if cls.is_first_tick:
            delay_sec = 1 / fps  # first tick will be wrong
            cls.is_first_tick = False
            cls.then = now
        else:
            elapsed_time_since_last_call_sec = now - cls.then
            delay_sec = max(0, 1 / fps - elapsed_time_since_last_call_sec)
            cls.then = now
        dont_care = 0
        # print(int(1000*delay_sec))
        while time.time() - now <= delay_sec:
            # update all handwriter sprites
            # but wait for redraw and display update in main game loop
            cls.handwriter_sprites.update(dont_care)
        return int(
            1000 * (elapsed_time_since_last_call_sec + delay_sec)
        )  # pygame needs milliseconds
