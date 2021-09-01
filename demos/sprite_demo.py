# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 15:29:39 2021

@author: NerdyTurkey
"""

import os
from pathlib import Path

path = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(path))
from itertools import cycle
import pygame as pg
import pyhandwriter as ph
from sprites import Player, NPC, Rain
from scheduler import Scheduler


def add_outline(surf, colour, thickness):
    """
    Draws onto surf the outline of the image.
    """
    mask = pg.mask.from_surface(surf)
    outline_pts = mask.outline()
    pg.draw.polygon(surf, colour, outline_pts, thickness)


def main():
    """
    More fancy demo of HandWriterSprite class in pyhandwriter to give 
    a taste of its use in a dialogue system (speech/thought bubbles).
    
    To keep things simple, no attempt has been made to animate the 
    characters movement!
    
    Instructions:
    =============
    Use arrows to move Hamlet (the cat moves independently).

    The following commands control Hamlet's speech bubble:
        SPACE = pause/unpause 
        RETURN = hide/unhide
        R = Reset writing
        C = Change text
        F = Faster writing
        S = Slower writing
        Esc or close window = quit"
    )
    """
    FPS = 60
    WIDTH, HEIGHT = 960, 640

    PLAYER_LAYER = 10
    PLAYER_SPEED = 0.1
    PLAYER_START_POS = WIDTH // 2, HEIGHT - 40
    SPEED_CHANGE_FACTOR = 1.1

    CAT_LAYER = 20
    CAT_SPEED = 0.05
    CAT_START_POS = WIDTH // 2, HEIGHT

    # speech bubbles
    BUBBLE_PLAYER_LAYER = 15
    BUBBLE_PLAYER_SIZE = 450, 350

    BUBBLE_PLAYER_TEXTS = cycle(
        [
            "Alas, poor Yorick! I knew him, Horatio, a fellow of infinite jest, of most excellent fancy.",
            "He hath borne me on his back a thousand times",
            "and now, how abhorred in my imagination it is! My gorge rises at it.",
            "Here hung those lips that I have kissed I know not how oft.",
            "Where be your gibes now? Your gambols? Your songs?",
            "Your flashes of merriment that were wont to set the table on a roar ?",
            "Not one now to mock your own grinning? Quite chapfallen ?",
            "Now get you to my lady’s chamber and tell her, let her paint an inch thick",
            "...to this favor she must come. Make her laugh at that .",
        ]
    )

    BUBBLE_CAT_TEXTS = cycle(
        [
            "Shakespeare is not my bag baby",
            "He is scaring off all the mice",
            "How do I get off this screen ?",
            "Call me catty , but he really sux",
            "I wish I was more animated",
            "He should paws more often",
            "What a ham - let !",
            "Is that a mouse I see before me ?",
            "This is a bit fishy",
            "What a total numb skull",
        ]
    )
    BUBBLE_CAT_LAYER = 25
    BUBBLE_CAT_SIZE = 350, 200
    PAUSE_DURATION = 2000  # millisec

    NUM_RAINDROPS = 200  # 200
    RAIN_LAYER = 50

    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.mouse.set_visible(False)

    # Load background image and scale to screen size
    background = pg.image.load(os.path.join("demo_assets", "cem2.jpg")).convert_alpha()
    bg_w, bg_h = background.get_size()
    sf = WIDTH / bg_w if WIDTH / HEIGHT < bg_w / bg_h else HEIGHT / bg_h
    background = pg.transform.rotozoom(background, 0, sf)

    # container for sprites
    allsprites = pg.sprite.LayeredDirty()

    # player sprite
    player_img = pg.image.load(
        os.path.join("demo_assets", "hamlet.png")
    ).convert_alpha()
    player_img = pg.transform.rotozoom(player_img, 0, 0.6)
    add_outline(player_img, (150, 150, 150), 1)
    player_img.set_alpha(150)
    player = Player(
        allsprites,
        PLAYER_LAYER,
        screen.get_size(),
        img=player_img,
        pos=PLAYER_START_POS,
        speed=PLAYER_SPEED,
    )

    # cat sprite
    cat_img = pg.image.load(os.path.join("demo_assets", "cat.png")).convert_alpha()
    add_outline(cat_img, (150, 150, 150), 1)
    cat = NPC(
        allsprites,
        CAT_LAYER,
        screen.get_size(),
        img=cat_img,
        pos=CAT_START_POS,
        speed=CAT_SPEED,
    )

    # player's speech bubble
    bubble_player_img = pg.image.load(
        os.path.join("demo_assets", "scroll.png")
    ).convert_alpha()
    bubble_player_img = pg.transform.scale(bubble_player_img, BUBBLE_PLAYER_SIZE)

    bubble_player = ph.HandWriterSprite(
        allsprites,
        BUBBLE_PLAYER_LAYER,
        bubble_player_img,
        next(BUBBLE_PLAYER_TEXTS),
        text_rect=(40, 50, 400, 290),  # rel to surf
        colour=(0, 0, 0),
        pt_size=24,
        speed_mult=1,
        cursor="quill_dark",
        nib={"width": 2, "angle": 45},
    )

    # cat's thought bubble
    bubble_cat_img = pg.image.load(
        os.path.join("demo_assets", "thought_bubble.png")
    ).convert_alpha()
    bubble_cat_img = pg.transform.scale(bubble_cat_img, BUBBLE_CAT_SIZE)
    fish_bones_img = pg.image.load(
        os.path.join("demo_assets", "fish_bones.png")
    ).convert_alpha()
    bubble_cat = ph.HandWriterSprite(
        allsprites,
        BUBBLE_CAT_LAYER,
        bubble_cat_img,
        next(BUBBLE_CAT_TEXTS),
        hw_font="hw_brushscript",
        text_rect=(25, 5, 320, 170),  # rel to surf
        colour=(255, 255, 255),
        pt_size=36,
        speed_mult=1.5,
        cursor=fish_bones_img,
        cursor_sf=0.2,
    )

    # raindrop sprites
    [
        Rain(allsprites, RAIN_LAYER, screen.get_size(), angle=3)
        for _ in range(NUM_RAINDROPS)
    ]

    running = True
    paused = False
    hidden = False

    # I wrote this Scheduler class to make it easy to schedule a series
    # of consecutive events in a game loop after a start condition is met.
    # I may do a short video on this at some point.
    scheduler = Scheduler()

    # Main Game Loop
    while running:
        # instead of usual
        # dt = clock.tick()(FPS)
        # do following
        dt = ph.HandWriterSprite.tick(FPS)

        #   Check for user events
        events = pg.event.get()
        for e in events:

            if e.type == pg.QUIT:
                return

            if e.type == pg.KEYDOWN:

                if e.key == pg.K_ESCAPE:
                    return

                if e.key == pg.K_f:
                    # write faster
                    bubble_player.change_speed(SPEED_CHANGE_FACTOR)

                if e.key == pg.K_s:
                    # write slower
                    bubble_player.change_speed(1 / SPEED_CHANGE_FACTOR)

                if e.key == pg.K_r:
                    # reset writing
                    bubble_player.reset()

                if e.key == pg.K_SPACE:
                    if paused:
                        bubble_player.unpause()
                    else:
                        bubble_player.pause()
                    paused = not paused

                if e.key == pg.K_RETURN:
                    if hidden:
                        bubble_player.unhide()
                    else:
                        bubble_player.hide()
                    hidden = not hidden

                # Note: player and cat movement handled in their respective
                # sprite update methods (see sprites.py)

        # Update
        allsprites.update(dt)

        # Bubbles track characters
        bubble_player.rect.midbottom = (
            player.rect.midtop[0],
            player.rect.midtop[1] + 20,
        )
        bubble_cat.rect.midbottom = (cat.rect.midtop[0], cat.rect.midtop[1] + 20)

        # Draw
        rects = allsprites.draw(screen, background)
        pg.display.update(rects)

        # Set window caption
        if dt > 0:
            pg.display.set_caption(f"FPS = {1000 * 1 / dt:.0f}")

        if bubble_player.finished:
            bubble_player.change_text(next(BUBBLE_PLAYER_TEXTS))

        """
        Notes about schedule.update() call below: 
        
        When start condition is met, the events are processed in turn:
        
        After a delay of PAUSE_DURATION, bubble_cat.hide method is called  with 
        args = () and kwargs = {}
        
        Then after a delay of PAUSE_DURATION, bubble-cat.unhide method is called with
        args = () and kwargs = {}
        
        Then after zero delay, bubble_cat.change_text method is called with 
        args = (next(BUBBLE_CAT_TEXTS),), kwargs = {}
        """
        scheduler.update(
            bubble_cat.finished,  # start condition
            (PAUSE_DURATION, bubble_cat.hide, (), {}),  # event 1
            (PAUSE_DURATION, bubble_cat.unhide, (), {}),  # event 2
            (0, bubble_cat.change_text, (next(BUBBLE_CAT_TEXTS),), {}),  # event 3
        )


if __name__ == "__main__":
    main()
    pg.quit()
    sys.exit()
