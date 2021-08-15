# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 15:29:39 2021

@author: jwgti
"""

from pathlib import Path

path = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(path))
import pygame as pg
import pyhandwriter as ph
from sprites import Player, Rain


def bye():
    print("goodbye!")
    pg.quit()
    sys.exit()


def main():
    HELP_TEXT = (
        "LEFT/RIGHT arrows: move, SPACE: pause/unpause, "
        "RETURN: hide/unhide, R: Reset, F=Faster, S=Slower, Esc = quit"
    )
    FPS = 60
    WIDTH, HEIGHT = 960, 640
    NUM_RAINDROPS = 200
    SPEED_CHANGE_FACTOR = 1.1
    PLAYER_LAYER = 10
    BUBBLE_LAYER = 20
    RAIN_LAYER = 30
    SPEECH = (
        r"Alas, poor Yorick! I knew him, Horatio, a fellow of infinite "
        r"jest, of most excellent fancy."
    )

    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    # Load background image and scale to screen size
    background = pg.image.load("demo_assets/cem2.jpg").convert_alpha()
    bg_w, bg_h = background.get_size()
    sf = WIDTH / bg_w if WIDTH / HEIGHT < bg_w / bg_h else HEIGHT / bg_h
    background = pg.transform.rotozoom(background, 0, sf)

    # Spawn Sprites------------------------------------------------------------

    allsprites = pg.sprite.LayeredDirty()  # container for sprites

    #   player
    hamlet_img = pg.image.load("demo_assets/hamlet.png").convert_alpha()
    hamlet_img = pg.transform.rotozoom(hamlet_img, 0, 0.5)

    #   add outline to make image clearer against dark background
    hamlet_mask = pg.mask.from_surface(hamlet_img)
    hamlet_outline_pts = hamlet_mask.outline()
    pg.draw.polygon(hamlet_img, (150, 150, 150), hamlet_outline_pts, 1)
    # hamlet_img.set_alpha(150)
    player = Player(allsprites, PLAYER_LAYER, screen.get_size(), img=hamlet_img)

    #   speech bubble
    bubble_size = 450, 350
    # bubble_img = pg.image.load("assets/speech_bubble.png").convert_alpha()
    bubble_img = pg.image.load("demo_assets/scroll.png").convert_alpha()
    bubble_img = pg.transform.scale(bubble_img, bubble_size)
    # bubble_img = pg.Surface(bubble_size, pg.SRCALPHA)
    # pg.draw.rect(bubble_img, (255,255,255), bubble_img.get_rect())
    quill_img = pg.image.load("demo_assets/quilL_dark.png").convert_alpha()
    hw_sprite = ph.HandWriterSprite(
        allsprites,
        BUBBLE_LAYER,
        bubble_img,
        SPEECH,
        text_rect=(40, 50, 400, 290),  # rel to surf
        # text_rect = (40, 50, 450, 290), # rel to surf
        colour=(0, 0, 0),
        pt_size=24,
        # instantly=True,
        speed_mult=1,
        # cursor=quill_img,
        # cursor = None,
        cursor="quill_dark",
        nib={"width": 2, "angle": 45},
        # bg_col=(0,0,0,0),
    )

    hw_sprite2 = ph.HandWriterSprite(
        allsprites,
        BUBBLE_LAYER,
        bubble_img.copy(),
        SPEECH,
        text_rect=(40, 50, 400, 290),  # rel to surf
        # text_rect = (40, 50, 450, 290), # rel to surf
        colour=(0, 0, 0),
        pt_size=24,
        # instantly=True,
        speed_mult=2,
        # cursor=quill_img,
        # cursor = None,
        cursor="spray_can",
        nib={"width": 2, "angle": 45},
        # bg_col=(0,0,0,0),
    )

    # #   raindrops
    [
        Rain(allsprites, RAIN_LAYER, screen.get_size(), angle=3)
        for _ in range(NUM_RAINDROPS)
    ]

    # Main Game Loop---------------------------------------------------------

    running = True
    paused = False
    hidden = False
    while running:
        # dt = clock.tick()(FPS)
        dt = ph.HandWriterSprite.tick(FPS)

        events = pg.event.get()

        #   Check for user events
        for e in events:

            if e.type == pg.QUIT:
                bye()

            if e.type == pg.KEYDOWN:

                if e.key == pg.K_ESCAPE:
                    bye()

                if e.key == pg.K_f:
                    # write faster
                    hw_sprite.change_speed(SPEED_CHANGE_FACTOR)

                if e.key == pg.K_s:
                    # write slower
                    hw_sprite.change_speed(1 / SPEED_CHANGE_FACTOR)

                if e.key == pg.K_r:
                    # reset writing
                    hw_sprite.reset()

                if e.key == pg.K_SPACE:
                    if paused:
                        hw_sprite.unpause()
                    else:
                        hw_sprite.pause()
                    paused = not paused

                if e.key == pg.K_h:
                    # hide
                    hw_sprite.hide()

                if e.key == pg.K_RETURN:
                    if hidden:
                        hw_sprite.unhide()
                    else:
                        hw_sprite.hide()
                    hidden = not hidden

        #   Update
        allsprites.update(dt)

        # hw_sprite.rect.midbottom = player.rect.midtop
        hw_sprite.rect.bottomleft = player.rect.topright
        hw_sprite2.rect.bottomright = player.rect.topleft
        # hw_sprite.rect.center = player.rect.center

        #   Draw
        rects = allsprites.draw(screen, background)
        pg.display.update(rects)
        # pg.display.set_caption(f'FPS = {clock.get_fps():.0f} {HELP_TEXT}')
        if dt > 0:
            pg.display.set_caption(f"FPS = {1000*1/dt:.0f} {HELP_TEXT}")


if __name__ == "__main__":
    main()
    pg.quit()
    sys.exit()
