# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 15:29:39 2021

@author: NerdyTurkey
"""

from pathlib import Path

path = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(path))
import pygame as pg
import pyhandwriter as ph


def main():
    """
    Simple demo of HandWriterSprite class in pyhandwriter.
    
    An instance of this class is like a regular pygame sprite,
    but you can animate handwritten text onto it and control the animation
    by sending commands to the sprite.
    
    Instructions:
    =============
    Use arrows to move sprite
    SPACE = pause/unpause writing
    RETURN = hide/unhide sprite
    R = Reset writing
    C = Change text
    F = Faster writing
    S = Slower writing
    Esc or close window = quit"
    )
    """

    FPS = 60
    WIDTH, HEIGHT = 960, 640
    SPEED = 2  # sprite speed across screen
    SPEED_CHANGE_FACTOR = 1.1  # for changing handwriting speed

    SCREEN_COLOUR = 239, 111, 108
    SPRITE_COLOUR = 70, 87, 117
    LINE_COLOUR = 86, 227, 159

    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.mouse.set_visible(False)
    allsprites = pg.sprite.Group()  # container for sprites

    img = pg.Surface((450, 300))
    img.fill(SPRITE_COLOUR)
    text1 = "I am a \white{COOL} sprite with animated handwriting !"
    text2 = (
        r"I am happy \halfspeed{\bigger{\blue{`happy`}}}"
        r"\nI am excited \halfspeed{\bigger{\orange{`excited`}}}"
        r"\nI \bigger{\red{`heart`}} to sing \bigger{\yellow{`music`} \down{\yellow{`music`}}"
    )
    hw_sprite = ph.HandWriterSprite(
        allsprites,  # sprite group
        1,  # layer (don't care here)
        img,  # sprite image
        text1,  # text to be handwritten
        colour=LINE_COLOUR,  # 'line' colour
        pt_size=40,
        linewidth=2,
        cursor="pencil",
    )

    running = True
    paused = False
    hidden = False
    text = text1
    x, y = WIDTH // 2, HEIGHT // 2 # centre pos of sprite

    # Main Game Loop
    while running:
        # instead of usual
        # dt = clock.tick()(FPS)
        # do following
        dt = ph.HandWriterSprite.tick(FPS)

        # Check for user events
        events = pg.event.get()
        for e in events:

            if e.type == pg.QUIT:
                return

            if e.type == pg.KEYDOWN:

                if e.key == pg.K_ESCAPE:
                    return

                if e.key == pg.K_f:
                    # write (F)aster
                    hw_sprite.change_speed(SPEED_CHANGE_FACTOR)

                if e.key == pg.K_s:
                    # write (S)lower
                    hw_sprite.change_speed(1 / SPEED_CHANGE_FACTOR)

                if e.key == pg.K_r:
                    # (R)eset writing
                    hw_sprite.reset()

                if e.key == pg.K_c:
                    # (C)hange text
                    if text == text1:
                        text = text2
                    else:
                        text = text1
                    hw_sprite.change_text(text)

                if e.key == pg.K_SPACE:
                    if paused:
                        hw_sprite.unpause()
                    else:
                        hw_sprite.pause()
                    paused = not paused

                if e.key == pg.K_RETURN:
                    if hidden:
                        hw_sprite.unhide()
                    else:
                        hw_sprite.hide()
                    hidden = not hidden

        # Move sprite with arrow keys
        # 8-way movement, but diagonal speed not corrected
        keys = pg.key.get_pressed()
        x += (keys[pg.K_RIGHT] - keys[pg.K_LEFT]) * SPEED
        y += (keys[pg.K_DOWN] - keys[pg.K_UP]) * SPEED

        # Update
        allsprites.update(dt)

        # Crude screen wrap
        hw_sprite.rect.center = x % WIDTH, y % HEIGHT

        # Draw
        screen.fill(SCREEN_COLOUR)
        allsprites.draw(screen)
        pg.display.flip()

        # Set window caption
        if dt > 0:
            pg.display.set_caption(f"FPS = {1000 * 1 / dt:.0f}")

        # Finish condition
        if hw_sprite.finished:
            # code here will run when all the text has been handwritten
            pass


if __name__ == "__main__":
    main()
    pg.quit()
    sys.exit()
