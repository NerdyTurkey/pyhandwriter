# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 17:59:00 2020

@author: jt
"""

import os
import pygame as pg
from . import text_utils as tu
from . import file_utils as fu
from . import settings as s
from .fname_check import is_valid_fname
from .buffer_smooth import BufferSmooth

vec = pg.math.Vector2


def key_val(char):
    """
    Return the dict key for char to be used in the hw_dic
    """
    if len(char) > 1:
        return ord(s.PROPS_REC["not_recognised_char"])
    try:
        return ord(char)
    except:
        # something else went wrong!
        return ord(s.PROPS_REC["not_recognised_char"])


class Recorder:
    """
    Class to record your handwriting to make you own handwritten font.

    You can choose a font and then work your way through the character set
    either tracing each char or doing your owvn version.

    Each recorded character is saved as a separate path file.

    These can be loaded up when you instantiate a HandWriter object.

    Instructions:
    =============
    Use mouse (or pen/stylus) to draw the current character in the box.
    Your strokes are recorded when you hold the left mouse button down.
    You can release  mouse button to move to the start of next stroke.

    Keys:

    Del to delete your current attempt.

    'N' to move to next character

    'P' to go back to previous character

    'S' to save (you can overwrite previous attempts)
         the path file will be linked to the current prompt character
         the path file has the following format:
             <your_font_name> + str(unicode of promptcharacter) + '.pth'
             e.g. if your font_name is 'my_font' and the prompt char is 'a'
             the path file will be 'my_font97.pth'
             When you use handwriter with 'my_font', all 'a's will be rendered
             with your handwritten version.

    'A' to save as
        You can handwrite anything - there is no checking against the prompt or
        trace char for accuracy!
        So if you want to create a custom symbol, use the "Save As" option to
        save it to a path file of your choosing.
        e.g. if you want to make the Greek symbol alpha, then draw an alpha
        (ignore the prompt char) and then press 'A' to save as. You will be
        prompted for a filename. Enter "alpha" and the path file will be saved
        to a folder containing custom symbols. You can use these custom symbols
        in any handwritten font by embedding the symbol name into the text to
        be written using backticks (like markdown)
        e.g. r'The first letter of the Greek alphabet is `alpha`'

    Return to preview your current handwritten character

    Esc (or close window) to quit.

    Note: if you skip some chars, then default handwritten characters will be
    rendered for the missing chars when you use your font.

    Params:
    ------
    screen: pygame surface
    The current display surface

    save_fname: string
    The root fname for saving your handwritten characters

    path: string
    The folder pathname to save font; if omitted default folder is used.

    prompt_font: pygame font or fontname
    Font for tracing or prompting

    fps: int
    Frames per second. Larger values increase sampling rate of your
    handwritten character.

    chars: list of chars
    The recording list of chars.
    The default is COMMON_CHARS which is the lower case letters, the upper case
    letters, the digits and most common punctuation and other symbols.
    Your can use your own list.

    Returns
    ------
    None

    """

    def __init__(
        self, screen, hw_font_save_fname, prompt_font=None, fps=None, chars=None
    ):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.hw_font_save_path = os.path.join(
            os.path.dirname(__file__), s.PROPS_GEN["hw_font_folder"]
        )
        self.hw_symbol_save_path = os.path.join(
            os.path.dirname(__file__), s.PROPS_GEN["hw_symbol_folder"]
        )
        self.hw_font_fname_root = os.path.join(
            self.hw_font_save_path, hw_font_save_fname
        )
        self.hw_symbol_fname_root = os.path.join(
            self.hw_symbol_save_path, s.PROPS_GEN["hw_symbol_fname"]
        )
        self.font = s.PROPS_REC["prompt_font"] if prompt_font is None else prompt_font
        self.pt_size = s.PROPS_REC["pt_size"]
        self.SF = s.PROPS_REC["save_pt_size"] / self.pt_size
        self.chars = s.COMMON_CHARS if chars is None else chars
        self.fps = fps or s.PROPS_REC["fps"]
        # screen coords to anchor text origin
        self.sox = self.screen_width // 2 - s.PROPS_REC["box_horiz_offset"]
        self.soy = self.screen_height // 2 + s.PROPS_REC["box_vert_offset"]
        self.clock = pg.time.Clock()
        self.current_path = []
        self.current_path_smoothed = []
        self.all_paths = []
        self.recording = False
        self.running = True
        self.i = 0
        self.mouse_pos = None
        self.start_time = None
        self.now = None
        self.show_char = True
        self.show_box = True
        # If self.trace, the characters are displayed inside the writing box for
        # tracing. Else they are displayed to the side as a prompt
        self.trace = True
        self.smooth_level = s.PROPS_REC["default_smooth_level"]
        self.smooth_value = s.PROPS_REC["smooth_levels"][self.smooth_level]
        self.bsx = BufferSmooth(self.smooth_value)
        self.bsy = BufferSmooth(self.smooth_value)

    def _start_recording(self):
        self.start_time = pg.time.get_ticks()
        self.recording = True

    def _stop_recording(self):
        self.recording = False
        self.all_paths.append(self.current_path)
        self.current_path = []

    def _next_char(self):
        self.current_path = []
        self.all_paths = []
        self.i += 1
        self.i %= len(self.chars)  # warp around

    def _previous_char(self):
        self.current_path = []
        self.all_paths = []
        self.i -= 1
        self.i %= len(self.chars)

    def _handwrite_it(self):
        self.screen.fill(s.PROPS_REC["bg_col"])

        for path in self.all_paths:
            self._draw_path(
                path,
                (self.sox + s.PROPS_REC["replay_offset"], self.soy),
                colour=s.PROPS_REC["replay_col"],
                scale=s.PROPS_REC["replay_scale"],
                speed_mult=s.PROPS_REC["replay_speed_mult"],
                linewidth=s.PROPS_REC["replay_linewidth"],
            )
        pg.time.delay(s.PROPS_REC["pause_ms"])

    def _delete(self):
        self.current_path = []
        self.all_paths = []

    def _save(self, fname):
        if self.all_paths:
            self._display_msg("Saving...")
            fu.pickle_dump(self.all_paths, fname)
            pg.time.delay(s.PROPS_REC["pause_ms"])

    def _save_as(self):
        # erase prompt char since not relevant for a save as
        self.show_char = False
        self.screen.fill(s.PROPS_REC["bg_col"])
        self._update_screen()
        pg.display.flip()
        self.show_char = True
        text_rect = tu.blit_text(
            "Enter filename :",
            self.screen,
            offset=s.PROPS_REC["save_as_offset"],
            text_handle="topleft",
            surf_handle="bottomleft",
            pt_size=s.PROPS_REC["msg_pt_size"],
        )
        pg.display.update(text_rect)
        fname = tu.get_text_input(
            self.screen,
            font=s.PROPS_REC["text_input_font"],
            text_size=s.PROPS_REC["msg_pt_size"],
            max_len=s.PROPS_REC["text_input_max_len"],
            text_color=s.PROPS_REC["text_input_col"],
            topleft=(text_rect.right, text_rect.top + 5),
        )
        if is_valid_fname(fname):
            full_fname = (
                self.hw_symbol_fname_root
                + s.PROPS_GEN["fname_separator"]
                + fname
                + ".pth"
            )
            if fu.file_exists(full_fname):
                text_rect = self._display_msg("File exists. Overwrite (y/n) ?")
                response = tu.get_text_input(
                    self.screen,
                    font=s.PROPS_REC["text_input_font"],
                    text_size=s.PROPS_REC["msg_pt_size"],
                    max_len=1,
                    text_color=s.PROPS_REC["text_input_col"],
                    topleft=(text_rect.right + 10, text_rect.top + 10),
                )
                if response is None:
                    return
                if response.lower() != "y":
                    self._display_msg("Not saved.")
                    pg.time.delay(s.PROPS_REC["pause_ms"])
                    return
            self._save(full_fname)
            return
        else:
            self._display_msg("Invalid filename !")
            pg.time.delay(s.PROPS_REC["pause_ms"])

    def _display_msg(self, msg):
        msg_rect = pg.Rect(
            0,
            s.PROPS_REC["msg_offset"][1],
            self.screen_width,
            s.PROPS_REC["msg_height"],
        )
        self.screen.fill(s.PROPS_REC["bg_col"], msg_rect)  # clear msg area
        text_rect = tu.blit_text(
            msg,
            self.screen,
            offset=s.PROPS_REC["msg_offset"],
            text_handle="midtop",
            surf_handle="midtop",
            pt_size=s.PROPS_REC["msg_pt_size"],
        )
        pg.display.update(msg_rect)
        return text_rect

    def _reset_smoothing(self, buffer_size=None):
        self.bsx.reset(buffer_size)
        self.bsy.reset(buffer_size)

    def _process_events(self):
        self.mouse_pos = pg.mouse.get_pos()
        for e in pg.event.get():
            if e.type == pg.MOUSEBUTTONDOWN:
                self._start_recording()
            elif e.type == pg.MOUSEBUTTONUP:
                self._reset_smoothing()
                self._stop_recording()
            if e.type == pg.QUIT:
                self.running = False
            elif e.type == pg.KEYUP:
                if e.key == pg.K_ESCAPE:
                    self.running = False
                try:
                    key_num = int(pg.key.name(e.key))
                except ValueError:
                    key_num = None
                if key_num in s.PROPS_REC["smooth_levels"]:
                    self.smooth_level = key_num
                    self.smooth_value = s.PROPS_REC["smooth_levels"][key_num]
                    self._reset_smoothing(self.smooth_value)
                    print(self.smooth_value)  # debug
                elif e.key == pg.K_n:
                    self._reset_smoothing()
                    self._next_char()
                elif e.key == pg.K_p:
                    self._reset_smoothing()
                    self._previous_char()
                elif e.key == pg.K_SPACE:
                    self._reset_smoothing()
                    self._handwrite_it()
                elif e.key == pg.K_DELETE:
                    self._reset_smoothing()
                    self._delete()
                elif e.key == pg.K_s:
                    self._reset_smoothing()
                    self._save(
                        self.hw_font_fname_root
                        + s.PROPS_GEN["fname_separator"]
                        + str(key_val(self.chars[self.i]))
                        + ".pth"
                    )
                    self._next_char()
                elif e.key == pg.K_a:
                    self._reset_smoothing()
                    self._save_as()
                    self._next_char()
                elif e.key in [pg.K_RALT, pg.K_LALT]:
                    self.trace = not self.trace
                elif e.key == pg.K_b:
                    self.show_box = not self.show_box

    def _record(self):
        if self.recording:
            self.now = pg.time.get_ticks()
            # dict allows more path params to be stored in future
            self.current_path.append(
                {
                    "pos": (
                        self.bsx.smooth((self.mouse_pos[0] - self.sox) * self.SF),
                        self.bsy.smooth((self.mouse_pos[1] - self.soy) * self.SF),
                    ),
                    "time": self.now - self.start_time,
                }
            )

    def _title(self):
        if self.trace:
            self.title_text = s.PROPS_REC["trace_title_text"]
        else:
            self.title_text = s.PROPS_REC["prompt_title_text"]
        tu.blit_text(
            self.title_text,
            self.screen,
            offset=s.PROPS_REC["title_offset"],
            text_handle="midtop",
            surf_handle="midtop",
            pt_size=s.PROPS_REC["title_pt_size"],
        )

    def _char_and_box(self):
        # ox,oy is char "origin" i.e. where char sits on line
        text_surf, (ox, oy) = tu.get_text_surface(
            text=self.chars[self.i],
            text_size=self.pt_size,
            text_font_name=self.font,
            text_col=s.PROPS_REC["sample_col"],
            bgnd_col=None,
            pad=5,
            show_origin=True,
        )
        box_rect = text_surf.get_rect()
        box_rect.topleft = self.sox - ox, self.soy - oy
        char_rect = pg.Rect(box_rect)
        if not self.trace:
            # prompt mode, char is to the left of box
            char_rect.right = char_rect.left - s.PROPS_REC["prompt_horiz_offset"]
        if self.show_char:
            # blit char
            self.screen.blit(text_surf, char_rect)
        if self.show_box:
            # draw box
            pg.draw.rect(self.screen, s.PROPS_REC["box_col"], box_rect, 1)

    def _current_path(self):
        self._draw_path(
            self.current_path,
            (self.sox, self.soy),
            colour=s.PROPS_REC["trace_col"],
            linewidth=s.PROPS_REC["trace_linewidth"],
            scale=1 / self.SF,
            instantly=True,
        )

    def _all_paths(self):
        for path in self.all_paths:
            self._draw_path(
                path,
                (self.sox, self.soy),
                colour=s.PROPS_REC["trace_col"],
                linewidth=s.PROPS_REC["trace_linewidth"],
                scale=1 / self.SF,
                instantly=True,
            )

    def _guideline(self):
        pg.draw.line(
            self.screen,
            s.PROPS_REC["ruler_col"],
            (0, self.soy),
            (self.screen_width, self.soy),
            1,
        )

    def _cursor(self):
        pg.draw.circle(
            self.screen,
            s.PROPS_REC["cursor_col"],
            self.mouse_pos,
            s.PROPS_REC["cursor_radius"],
            s.PROPS_REC["cursor_linewidth"],
        )

    def _help(self):
        tu.blit_text(
            s.PROPS_REC["help_text0"],
            self.screen,
            offset=s.PROPS_REC["help_offset0"],
            text_handle="midbottom",
            surf_handle="midbottom",
            pt_size=s.PROPS_REC["help_pt_size"],
        )
        tu.blit_text(
            s.PROPS_REC["help_text1"],
            self.screen,
            offset=s.PROPS_REC["help_offset1"],
            text_handle="midbottom",
            surf_handle="midbottom",
            pt_size=s.PROPS_REC["help_pt_size"],
        )

    def _smooth_value(self):
        tu.blit_text(
            "smooth level = " + str(self.smooth_level),
            self.screen,
            offset=s.PROPS_REC["smooth_offset"],
            text_handle="midbottom",
            surf_handle="midbottom",
            pt_size=s.PROPS_REC["smooth_pt_size"],
        )

    def _update_screen(self):
        self._title()
        self._smooth_value()
        self._char_and_box()
        self._current_path()
        self._all_paths()
        self._guideline()
        self._cursor()
        self._help()

    def _draw_path(
        self,
        path,
        origin_pos,
        colour=None,
        linewidth=None,
        scale=None,
        speed_mult=None,
        instantly=False,
        cursor_img=None,
    ):
        """
        Draws a path to screen using the timing info encoded with the path
        to replicate the recorded stroke. A char will often comprise multiple
        paths.
        """
        if path == []:
            return
        # Since _draw_path only called internally, do not worry about default
        # values for keyword args. Will crash if one or more is NOT passed!
        sox, soy = origin_pos
        x_max = 0  # leftmost part of path
        if cursor_img is not None:
            cursor_rect = cursor_img.get_rect()
            # to save region under cursor img
            save_surf = pg.Surface((cursor_rect.w, cursor_rect.h))
        for (i, data) in enumerate(path[:-1]):
            current_pt = (sox + scale * data["pos"][0], soy + scale * data["pos"][1])
            current_time = data["time"]
            next_pt = (
                sox + scale * path[i + 1]["pos"][0],
                soy + scale * path[i + 1]["pos"][1],
            )
            next_time = path[i + 1]["time"]
            modified_rect = pg.draw.line(
                self.screen, colour, current_pt, next_pt, linewidth
            )
            if not instantly:
                if cursor_img is not None:
                    cursor_rect.topleft = next_pt
                    # save screen under cursor surf
                    save_surf.blit(self.screen, (0, 0), cursor_rect)
                    # blit cursor
                    self.screen.blit(cursor_img, cursor_rect)
                    # update that region so it shows
                    pg.display.update(cursor_rect)

                # Only updates modified part of display.
                # MUCH faster than pg.display.flip()!
                pg.display.update(modified_rect)
                pg.time.delay(int((next_time - current_time) / speed_mult))
                if cursor_img is not None:
                    # restore saved region
                    self.screen.blit(save_surf, cursor_rect)
                    pg.display.update(cursor_rect)
            if current_pt[0] > x_max:
                x_max = current_pt[0]
            if next_pt[0] > x_max:
                x_max = next_pt[0]
        return x_max

    def record(self):
        while self.running:
            self._process_events()
            self.screen.fill(s.PROPS_REC["bg_col"])
            self._record()
            self._update_screen()
            pg.display.set_caption(
                f"actual FPS={self.clock.get_fps():.0f}, \
                                   desired FPS = {self.fps}"
            )
            pg.display.flip()
            self.clock.tick(self.fps)
