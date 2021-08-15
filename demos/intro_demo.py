# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:28:38 2020

@author: jt
"""
# Demo of pyhandwriter (as used in my first YouTube video on this).

import os
from pathlib import Path

path = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(path))

import pygame as pg

vec = pg.math.Vector2
import pyhandwriter as ph

START_PAGE = 1


def main():

    SF = 1.4
    WIDTH = int(SF * 900)
    HEIGHT = int(SF * 700)

    pg.init()
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("pyhandwriter: intro demo")
    screen.fill(ph.col("BLACK"))

    banana = pg.image.load(
        os.path.join("demo_assets", "banana.png")
    ).convert_alpha()  # ink will appear to come from topleft of image
    banana = pg.transform.rotozoom(banana, 0, 0.1)

    # Instantiate a Handwrite obj----------------------------------------------

    # ... use default font
    hw = ph.HandWriter(screen)
    # or use your own font, eg. "MyFont" previously recorded using recorder
    # hw = HandWriter(screen, hw_font="MyFont")

    pages = []  # a list of dicts, each dict is one text block = 1 'page'

    # Page 1------------------------------------------------------------------
    page = {}
    page["text"] = (
        r"\bigger{\bigger{\bold{\blue{handwriter. py} for \yellow{pygame}}}}"
        r"\n\nHello and welome !"
        r"\n\nI thought it would be fun, and maybe even useful, to write some code"
        r'that animates handwriting in pygame.\n\nThere are a few built in " fonts "'
        r"like this one that I made by recording my own handwriting."
        r"\nYou can also record your own handwriting using the same program."
    )
    page["topleft"] = 50, 50
    page["width"] = 770
    page["pt_size"] = 28
    page["cursor"] = "pencil"
    page["speed"] = 1
    page["hyphenation"] = False
    page["clear_screen"] = True

    pages.append(page)

    # Page 2------------------------------------------------------------------
    page = {}
    page["text"] = (
        r"Basic formatting is available, such as \bold{bold},"
        r" \underline{underline}, super\super{scripts}, and sub\sub{scripts} ."
        r"\n\nSuper and subs are useful for simple equations like E = mc\super{2} and"
        r" 3/2 k\sub{B}T.\n\n\red{A} \green{large} \blue{range} \yellow{of}"
        r" \magenta{common} \teal{colours} \lightgray{are} \coral{possible}.\n"
        r"\n\nAnd these formatting options can easily be combined, e.g."
        r" \underline{\bold{\cyan{bold cyan and underlined !}}}."
    )
    page["topleft"] = 50, 50
    page["width"] = 770
    page["pt_size"] = 28
    page["cursor"] = "pencil"
    page["speed"] = 1
    page["hyphenation"] = False
    page["clear_screen"] = True

    pages.append(page)

    # Page 3------------------------------------------------------------------
    page = {}
    page[
        "text"
    ] = r"\lime{The default cursor is this pencil. But you can change that to }"
    page["topleft"] = 50, 50
    page["width"] = 770
    page["pt_size"] = 28
    page["cursor"] = "pencil"
    page["speed"] = 1.5
    page["hyphenation"] = False
    page["clear_screen"] = False

    pages.append(page)

    # Page 4------------------------------------------------------------------
    page = {}
    page["text"] = r"A crosshair or "
    page["topleft"] = 50, 200
    page["width"] = 770
    page["pt_size"] = 28
    page["cursor"] = "crosshair"
    page["cursor_sf"] = 2
    page["speed"] = 1.5
    page["hyphenation"] = False
    page["clear_screen"] = False

    pages.append(page)

    # Page 5------------------------------------------------------------------
    page = {}
    page["text"] = r"a quill to give a historical vibe, or "
    page["topleft"] = 50, 300
    page["width"] = 770
    page["pt_size"] = 28
    page["cursor"] = "quill_light"
    page["cursor_sf"] = 1
    page["speed"] = 1
    page["hyphenation"] = False
    page["clear_screen"] = False

    pages.append(page)

    # Page 6------------------------------------------------------------------
    page = {}
    page["text"] = r"\red{an arrow, amongst built in cursors }"
    page["topleft"] = 50, 400
    page["width"] = 770
    page["pt_size"] = 28
    page["cursor"] = "arrow"
    page["cursor_sf"] = 2
    page["speed"] = 1
    page["hyphenation"] = False
    page["clear_screen"] = False

    pages.append(page)

    # Page 7------------------------------------------------------------------
    page = {}
    page["text"] = r"\lavender{or go bananas and change it to your own custom image !}"
    page["topleft"] = 50, 500
    page["width"] = 770
    page["pt_size"] = 28
    page["cursor"] = banana
    page["cursor_sf"] = 2
    page["speed"] = 1
    page["hyphenation"] = False
    page["clear_screen"] = True

    pages.append(page)

    # Page 8------------------------------------------------------------------
    page = {}
    page["text"] = (
        r"The writing speed is fully controllable.\n\doublespeed{You can"
        r" easily speed it up} \halfspeed{\halfspeed{or slow it down}}.\nYou can also add"
        r" a dramatic -- \p\ppause.\n\nA few useful symbols are included (you can"
        r" add more of your own), such as arrows  `left` `right` `up` `down` and some emojies:\n"
        r"I am happy\t\halfspeed{\green{\bigger{`happy`}}}\tI am sad\t\halfspeed{\blue{\bigger{`sad`}}}\n"
        r"I am bored\t\halfspeed{\bigger{`bored`}}\tI am excited\t\halfspeed{\orange{\bigger{`excited`}}}\n"
        r"I am confused\t\halfspeed{\pink{\bigger{`confused`}}}\n\nThe\ttab\tspaces\twere\teasy\tto\tdo !"
    )
    page["topleft"] = 50, 50
    page["width"] = 770
    page["pt_size"] = 28
    page["cursor"] = "pencil"
    page["speed"] = 1
    page["hyphenation"] = False
    page["clear_screen"] = True

    pages.append(page)

    # Page 9------------------------------------------------------------------
    page = {}
    page["text"] = (
        r"\yellow{You can make any text \bigger{\bigger{bigger}} or"
        r" \smaller{\smaller{smaller}}, or lift it \up{up} or \down{down}}.\n\n"
        r"\coral{The default is for words not be broken over a line. However this can lead"
        r" to a ragged right edge, especially if the text box is narrow.}"
    )
    page["topleft"] = 300, 30
    page["width"] = 300
    page["pt_size"] = 28
    page["cursor"] = "pencil"
    page["speed"] = 1
    page["hyphenation"] = False
    page["clear_screen"] = True

    pages.append(page)

    # Page 10-----------------------------------------------------------------
    page = {}
    page["text"] = (
        r"\yellow{So I implemented a crude hyphenation system, which breaks a word"
        r"when it gets too close to the right hand margin and inserts a hyphen at some"
        r"fairly random position in the word. I might improve that in the next version!\n\n}"
    )
    page["topleft"] = 250, 100
    page["width"] = 400
    page["pt_size"] = 28
    page["cursor"] = "pencil"
    page["speed"] = 1
    page["hyphenation"] = True
    page["clear_screen"] = True

    pages.append(page)

    # Page 121
    page = {}
    page["text"] = (
        r"A feature that took some \red{headscratching} to implement, but which I think will"
        r" be useful for lectures and tutorials are equations, which are entered as latex.\n\n"
        r"Here is an example of an inline one $a x^2 + b x + c = 0$  and here is a newline"
        r" one which gets automatically centred on a new line (let's make it pink for fun)"
        r"\pink{£x = \frac{-b\pm\sqrt{b^2-4 a c}}{2a}£}"
        r"These equations require a latex installation on your PC, but anyone wanting to"
        r" use them is likely to have that, I think."
    )
    page["topleft"] = 50, 50
    page["width"] = 770
    page["pt_size"] = 28
    page["cursor"] = "pencil"
    page["speed"] = 1
    page["hyphenation"] = False
    page["clear_screen"] = True

    pages.append(page)

    # Page 12-----------------------------------------------------------------
    page = {}
    page["text"] = (
        r"Anyway ,  I hope you found this interesting \bold{.} Maybe you have ideas"
        r"for how you could use it in a dialogue system for a game or for online tutorials.\n\n"
        r"If I get some likes/comments on this video I will follow up with some other"
        r" videos on how to  use this program and how I wrote it.\n\nI also plan to"
        r" make it available on itch \bold{.} io\n\nBye for now and thanks for watching"
        r"  \lime{\bigger{\bigger{`happy`}}}"
    )
    page["topleft"] = 50, 50
    page["width"] = 770
    page["pt_size"] = 28
    page["cursor"] = "pencil"
    page["speed"] = 1
    page["hyphenation"] = False
    page["clear_screen"] = True

    pages.append(page)

    # hit a key to start
    waiting = True
    while waiting:
        for e in pg.event.get():
            if e.type == pg.KEYUP:
                waiting = False

    for page in range(START_PAGE - 1, len(pages)):
        pg.display.flip()

        p = pages[page]
        text_rect = pg.Rect(
            int(SF * p["topleft"][0]),
            int(SF * p["topleft"][1]),
            int(SF * p["width"]),
            HEIGHT,
        )
        ret = hw.write_text(
            p["text"],
            text_rect=text_rect,
            pt_size=int(SF * p["pt_size"]),
            speed_mult=p["speed"],
            # smooth_level=4,
            instantly=False,
            cursor=p["cursor"],
            cursor_sf=p.get("cursor_sf"),
            num_tabs=6,
            hyphenation=p["hyphenation"],
            nib={"width": 4, "angle": 45},
            # surf_bg_col=(255,255,255,100),
            # surf_border_width=5,
            # surf_border_col=(255,0,0,255),
            # text_rect_bg_col=(0,0,255,255 ),
            # text_rect_border_width=10,
            # text_rect_border_col=(0,255,255,255),
        )

        if ret is ph.Flag.USER_QUIT:
            # quit during write_text
            return

        if ret is ph.Flag.OVERFLOW:
            # text overflowed text rect
            print("Text overflow")
            pass

        # wait for quit or next page
        waiting = True
        while waiting:
            for e in pg.event.get():
                if e.type == pg.KEYUP:
                    waiting = False
                    if p["clear_screen"]:
                        screen.fill(ph.col("BLACK"))
                    pg.display.flip()
                    break
                if e.type == pg.QUIT:
                    return


if __name__ == "__main__":
    main()
    pg.quit()
    sys.exit()
