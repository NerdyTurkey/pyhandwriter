# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 17:59:00 2020

@author: NerdyTurkey
"""
import os
import time
import warnings
from copy import deepcopy

import pygame as pg

from . import colours
from . import config
from . import file_utils as fu
from . import legal_token_check
from . import settings as s
from . import style_tokens
from .brack_delimit_parser import delimiter_parse
from .buffer_smooth import BufferSmooth
from .check_user_event import check_user_event, UserEvent
from .colorize import colorize
from .convert_image_to_surface import convert_image_to_surface
from .enums import Flag
from .latex_to_img import latex_to_img
from .line_blit import line_blit
from .my_parser import parse
from .rescale_surf import rescale_surf
from .set_alpha import set_alpha

vec = pg.math.Vector2


def oneshot_generator(val):
    yield val


class Container:
    """
    For grouping attributes. I think sometimes neater than dictionaries
    """


def get_char_key(char):
    """
    Return the dict key for a regular char to be used in the hw_dic.
    This is the str of the unicode of char.
    Note: that char_key for a symbols is the symbol name and are generated
    elsewhere.
    """
    try:
        return str(ord(char))
    except:
        # something went wrong!
        return str(ord("?"))


def get_tab_stop(x, tab_spacing):
    """
    Returns next tab stop when cursor is at horiz pos x
    """
    return (x // tab_spacing) * tab_spacing + tab_spacing * (x % tab_spacing > 0)


class HandWriterGen:
    """
    The generator version of the Handwriter class.
    """

    def __init__(self, surf, hw_font=None):
        self.surf = surf

        # Working hw font dictionary is self.hw_dict
        # If user hw_font is None this defaults to self.hw_default_dict.
        # self.hw_default_dict is also used to replace in missing
        # chars from user hw_font.

        # The char sizes (in x an y) are stored in separate dictionaries
        # self.char_sizes and self.default_char_sizes for self.hw_dict and
        # self.hw_default_dict, respectively.

        # Presently, all hw_fonts are stored in the same folder inside the
        # package.
        font_path = os.path.join(
            os.path.dirname(__file__), s.PROPS_GEN["hw_font_folder"]
        )
        self.hw_default_dict = self._load_hw_dict(
            s.PROPS_GEN["default_hw_font"], font_path
        )
        if hw_font is None:
            self.hw_dict = deepcopy(self.hw_default_dict)
        else:
            # load user hw font
            self.hw_dict = self._load_hw_dict(hw_font, font_path)

        # load symbols, i.e. handwritten versions on non standard chars
        # both built-ins (like arrows and emojis) and user symbols made with
        # recorder.py

        # Presently, all hw_symbols are stores in the same folder insider the
        # package.
        symbol_path = os.path.join(
            os.path.dirname(__file__), s.PROPS_GEN["hw_symbol_folder"]
        )
        symbols_dict = self._load_hw_dict(s.PROPS_GEN["hw_symbol_fname"], symbol_path)
        # add symbols dict to main dict
        self.hw_dict = {**self.hw_dict, **symbols_dict}

        # Make a backup to revert to if original is changed (e.g. smoothed)
        # and user wants to undo change.
        self.hw_dict0 = deepcopy(self.hw_dict)

        self.default_char_sizes = self.get_char_sizes(self.hw_default_dict)
        self.char_sizes = self.get_char_sizes(self.hw_dict)

        # This is used for line breaking calculations
        self.generic_char_size = self.char_sizes.get(
            get_char_key("W"), self.default_char_sizes[get_char_key("W")]
        )

        self._load_cursors()

        self._load_spray()

    def _load_cursors(self):
        self.cursors = {}
        for name, fname in s.CURSORS.items():
            self.cursors[name] = pg.image.load(fname).convert_alpha()

    def _load_spray(self):
        path = os.path.join(os.path.dirname(__file__), "assets")
        spray_fname = os.path.join(path, "spray_softer.png")
        self.spray = pg.image.load(spray_fname).convert_alpha()

    def _customise_spray(self, spray_props):
        width = 2 * spray_props["width"]
        col = spray_props["col"]
        aspect_ratio = spray_props["aspect_ratio"]
        angle = spray_props["angle"]
        self.spray = colorize(self.spray, col)
        self.spray = pg.transform.scale(self.spray, (width, int(width / aspect_ratio)))
        self.spray = pg.transform.rotate(self.spray, angle)
        if len(col) == 4:
            # apply alpha
            self.spray = set_alpha(self.spray, col[3])

    def change_surf(self, surf):
        self.surf = surf

    def _load_hw_dict(self, hw_font, path):
        """
        Creates a hw_dict by loading pre-recorded path files.
        a hw_dict has keys that are unicodes* of char and values that is the
        path data for rendering them.
        A path file contains (x,y) cordinates for the handwritten strokes
        making up a character together with the sample times.
        *For a special char (like emojies and arrows or user recorded symbols),
        the key is the names of the symbol.
        """

        hw_dict = {}
        # get list of all filenames starting with the hw_font string
        filenames = fu.get_filenames_with_prefix(hw_font, path=path)

        if not filenames:
            raise Exception(hw_font + " not found!")

        for filename in filenames:
            fname, ext = filename.split(".")

            if ext != "pth":
                continue

            result = fu.pickle_load(os.path.join(path, filename))

            if result is Flag.FAIL:
                # pickle load failed
                continue

            else:
                char_key = fname[
                    -(len(fname) - len(hw_font) - len(s.PROPS_GEN["fname_separator"])) :
                ]
                # print(char_key) # debug
                hw_dict[char_key] = result

        # The hw_dict will only contain a key,val entry if the
        # corresponding pth file could be loaded properly.
        # Missing keys will be handled by write_text method.
        # A valid key is either str of unicode for a "regular" char
        # or a symbol name, e.g. built-in symbols "left", "happy".

        return hw_dict

    def get_char_sizes(self, hw_dict):
        """
        Returns a dictionary with keys the char "unicodes" and values
        a tuple giving the (x,y) extent of the paths in pixels.
        """
        # ToDo: rather than separate dict, this could be added to hw_dict
        char_sizes = {}
        for key, paths in hw_dict.items():

            for path in paths:
                x_pts = [data["pos"][0] for data in path]
                y_pts = [data["pos"][1] for data in path]

            char_sizes[key] = (
                abs(min(x_pts) - max(x_pts)),
                abs(min(y_pts) - max(y_pts)),
            )

        return char_sizes

    def _draw_path(
        self,
        path,
        origin_pos,
        colour=None,
        linewidth=None,
        nib=None,
        spray=None,
        scale=None,
        speed_mult=None,
        instantly=False,
        cursor_img=None,
    ):
        """
        Draws a path to surf using the timing info encoded with the path
        to replicate the recorded stroke. A char will often comprise multiple
        paths.
        Generator. Yields None until the path is finished and the yields x_max
        """

        # ---------------------------------------------------------------------
        def delay_gen(delay_ms):
            if instantly:
                # single-shot generator
                yield
                return
            delay_s = delay_ms / 1000
            start_time = time.time()
            while time.time() - start_time < delay_s:
                yield

        # ---------------------------------------------------------------------
        if path == []:
            yield
        if cursor_img is not None:
            cursor_rect = cursor_img.get_rect()

            # make a surf for saving region under cursor img
            save_surf = pg.Surface(cursor_rect.size, pg.SRCALPHA)

        sox, soy = origin_pos
        colour = colour or s.PROPS_GEN["colour"]
        linewidth = linewidth or s.PROPS_GEN["linewidth"]
        speed_mult = speed_mult or s.PROPS_GEN["speed_mult"]
        scale = scale or s.PROPS_GEN["scale"]
        x_max = 0  # leftmost part of path

        for (i, data) in enumerate(path[:-1]):
            current_pt = vec(
                (sox + scale * data["pos"][0], soy + scale * data["pos"][1])
            )
            current_time = data["time"]
            next_pt = vec(
                (
                    sox + scale * path[i + 1]["pos"][0],
                    soy + scale * path[i + 1]["pos"][1],
                )
            )
            next_time = path[i + 1]["time"]

            # restore surf under cursor, but not on first pass
            if not instantly and cursor_img is not None and i != 0:
                self.surf.fill(
                    (0, 0, 0, 0), cursor_rect
                )  # wipe surf under cursor first
                self.surf.blit(save_surf, cursor_rect)  # restore saved surf

            # draw path segment
            if nib is not None:
                # calligraphy type stroke
                # parallelogram shape
                # work out poly pts
                offset = nib["width"] * vec(0, 1).rotate(nib["angle"])
                current_pt2 = current_pt + offset
                next_pt2 = next_pt + offset
                poly_pts = [current_pt, current_pt2, next_pt2, next_pt]
                modified_rect = pg.draw.polygon(self.surf, colour, poly_pts)
            elif spray is not None:
                # ToDo: nib currently trumps spray; do I want that?
                # path point is at centre of spray
                modified_rect = line_blit(self.surf, current_pt, next_pt, self.spray)
            else:
                # regular line
                modified_rect = pg.draw.line(
                    self.surf, colour, current_pt, next_pt, linewidth
                )

            # no cursor drawn if handwriting rendered 'instantly'
            if not instantly:

                # update cursor position
                if cursor_img is not None:
                    cursor_rect.topleft = next_pt

                    # save surf region under new cursor pos before it is blitted
                    save_surf.fill((0, 0, 0, 0))  # wipe save_surf first
                    save_surf.blit(self.surf, (0, 0), cursor_rect)

                    # blit cursor
                    self.surf.blit(cursor_img, cursor_rect)

                    if self.update_display:
                        pg.display.update(cursor_rect)

                # update display where ink has been laid (line, nib or spray)
                if self.update_display:
                    pg.display.update(modified_rect)
                delay_ms = (next_time - current_time) / speed_mult
                dg = delay_gen(delay_ms)

                while True:
                    try:
                        next(dg)
                        yield
                    except StopIteration:
                        break

            # clean-up at end of path
            if not instantly and cursor_img is not None:
                # restore surf under cursor
                self.surf.fill((0, 0, 0, 0), cursor_rect)  # wipe it first
                self.surf.blit(save_surf, cursor_rect)
                if self.update_display:
                    pg.display.update(cursor_rect)

            if current_pt[0] > x_max:
                x_max = current_pt[0]

            if next_pt[0] > x_max:
                x_max = next_pt[0]

        # clean-up at end of path
        if not instantly and cursor_img is not None:
            # restore surf under cursor
            self.surf.fill((0, 0, 0, 0), cursor_rect)  # wipe it first
            self.surf.blit(save_surf, cursor_rect)
            if self.update_display:
                # calling code is using screen as surf
                # so need to update display
                pg.display.update(cursor_rect)

        yield x_max

    def _get_word_length_pixels(self, parsed_text, j, norm_scale):
        """
        Return length in pixels of word in parsed text starting at
        index j
        """
        length = 0
        # temp_string = '' # debug

        while j < len(parsed_text) and parsed_text[j][1] != " ":

            if parsed_text[j][1] == "\\":
                j += 2
                continue
            char_size = self.char_sizes.get(
                parsed_text[j][1],
                (
                    self.default_char_sizes.get(
                        parsed_text[j][1], self.generic_char_size
                    )
                ),
            )
            char_width = char_size[0]
            length += char_width * norm_scale
            # temp_string += parsed_text[j][1] # debug

            j += 1

        return length

    def _preprocess_text(self, text):
        """
        Parses latex control chars, symbol control chars, and tabs
        """
        # ToDo change $, £ etc to consts in settings
        self.props.latex_inline_list, text = delimiter_parse(
            text, delimiter="$", repl_string="\\$"
        )
        self.props.latex_newline_list, text = delimiter_parse(
            text, delimiter="£", repl_string="\\£"
        )

        self.props.symbol_list, text = delimiter_parse(
            text, delimiter=s.SYMBOL_ESC_CHAR, repl_string="\\" + s.SYMBOL_ESC_CHAR
        )

        return text.replace("\\t", " \\t")  # note space in 2nd arg

    def _process_style(self):
        """
        Apply formatting style
        """
        # print(f"{self.state.style_set=}") # debug
        if "bigger" in self.state.style_set:
            self.style.scale *= s.PROPS_GEN["scale_multipler"]

        if "smaller" in self.state.style_set:
            self.style.scale /= s.PROPS_GEN["scale_multipler"]

        if "bold" in self.state.style_set:
            self.style.linewidth *= s.PROPS_GEN["bold_linewidth_sf"]

        if "super" in self.state.style_set:
            self.style.vert_offset += self.props.super_offset
            self.style.scale *= s.PROPS_GEN["super_size_sf"]

        if "sub" in self.state.style_set:
            self.style.vert_offset += self.props.sub_offset
            self.style.scale *= s.PROPS_GEN["sub_size_sf"]

        if "up" in self.state.style_set:
            self.style.vert_offset += self.props.up_offset

        if "down" in self.state.style_set:
            self.style.vert_offset += self.props.down_offset

        for col, rgb in colours.col_dict.items():

            if col.lower() in self.state.style_set:
                self.style.colour = rgb
                # No ordering in set, so if mult colours set,
                # random one will be selected!
                break

        if "underline" in self.state.style_set:
            # save current pos to know where underline should start
            self.state.underline_start_pos = (
                self.state.current_pos[0],
                self.state.current_pos[1] + s.PROPS_GEN["underline_offset"],
            )

        if "doublespeed" in self.state.style_set:
            self.style.speed_mult *= 2

        if "halfspeed" in self.state.style_set:
            self.style.speed_mult *= 0.5

    def _process_formatting_esc_char(self, char):
        """
        Processes formatting-type Esc chars, returns None if ready to move
        to next char or the new processed char to write.
        """

        if char == "n":
            # newline
            self._newline()

        elif char == "t":
            # tab
            tab_pos = self.props.origin_pos[0] + get_tab_stop(
                self.state.current_pos[0] - self.props.origin_pos[0],
                self.props.tab_spacing,
            )

            if tab_pos >= (self.props.text_box_width - s.PROPS_GEN["text_box_margin"]):
                self._newline()

            else:
                self.state.current_pos = tab_pos, self.state.current_pos[1]

        return None

    def _process_symbol_esc_char(self, char):
        """
        Processes symbol-type Esc chars, returns None if ready to move
        to next char or the char_key to write.
        """

        if char == s.SYMBOL_ESC_CHAR:
            char_key = self.props.symbol_list[self.state.symbol_count]
            self.state.symbol_count += 1
            # print(char_key) # debug
            return char_key

        return None

    def _init_latex_process(self, char):
        """
        Returns the latex and a vertical height adjustment dependent on char

        """
        if char == "$":
            # This is inline latex equation
            latex = self.props.latex_inline_list[self.state.latex_inline_count]
            self.state.latex_inline_count += 1
            height_tweak = s.PROPS_GEN["latex_inline_height_scaling"]

        elif char == "£":
            # This is newline latex equation (like $$xx$$)
            latex = self.props.latex_newline_list[self.state.latex_newline_count]
            self.state.latex_newline_count += 1
            height_tweak = s.PROPS_GEN["latex_newline_height_scaling"]

        return latex, height_tweak

    def _get_latex_surf(self, latex, height_tweak):
        """
        Returns a pygame surface with latext rendered on it
        """
        try:
            latex_img = latex_to_img(
                latex,
                pt_size=self.props.pt_size,
                text_col=self.style.colour,
                bg_col=self.props.text_rect_bg_col,
            )
        except:
            msg = "Latex could not be rendered because :"
            if "matplotlib" in config.failed_imports:
                msg = "Matplotlib could not be imported."
            elif "PIL" in config.failed_imports:
                msg += "PIL could not be imported"
            else:
                msg += "No latex installation found on your computer."
            warnings.warn(msg)
            return None

        latex_surf = convert_image_to_surface(latex_img)

        # scale latex_surf so height matches pt_size with tweak factor
        latex_surf = rescale_surf(latex_surf, height=height_tweak * self.props.pt_size)

        if "bigger" in self.state.style_set:
            latex_surf = pg.transform.rotozoom(latex_surf, 0, 2)

        elif "smaller" in self.state.style_set:
            latex_surf = pg.transform.rotozoom(latex_surf, 0, 0.5)

        return latex_surf

    def _get_scaled_latex_surf(self, char, latex_surf):
        """
        Returns latex_surf scaled to correct size
        """
        # get rect and dimesions
        latex_rect = latex_surf.get_rect()
        w, h = latex_rect.size

        if char == "$":
            # inline eqn
            # check if latex_surf too long for current line
            if self.state.current_pos[0] + w >= self.props.text_box_left_edge:
                self._newline()

                # rescale to fit onto newline if necessary
                if w > self.props.text_box_width:
                    # scale to fit onto one line
                    latex_surf = rescale_surf(
                        latex_surf,
                        width=s.PROPS_GEN["latex_full_line_scaling"]
                        * self.props.text_box_width,
                    )

        if char == "£":
            # centred, newline eqn
            # rescale to fit onto newline if necessary
            if w > self.props.text_box_width:
                # scale to fit onto one line
                latex_surf = rescale_surf(
                    latex_surf,
                    width=s.PROPS_GEN["latex_full_line_scaling"]
                    * self.props.text_box_width,
                )

        return latex_surf

    def _process_latex_position(self, char, w, h):
        """
        Ensures newline latex equations £..£ are centred on newline.
        """
        if char == "£":
            # centre on new line
            self.state.current_pos = (
                self.props.origin_pos[0] + (self.props.text_box_width - w) // 2,
                self.state.current_pos[1]
                + self.props.line_spacing
                + s.PROPS_GEN["latex_newline_vert_padding"],
            )

    def _blit_latex(self, latex_surf, latex_rect):
        """
        Blits the latex surf to the surf.
        """
        latex_rect.bottomleft = (
            self.state.current_pos[0]
            + self.props.pt_size * s.PROPS_GEN["latex_horiz_spacing_multiplier"],
            self.state.current_pos[1]
            + self.props.pt_size * s.PROPS_GEN["latex_inline_vert_offset_multiplier"],
        )

        mod_rect = self.surf.blit(latex_surf, latex_rect)
        if self.update_display:
            pg.display.update(mod_rect)

    def _move_to_next_position(self, char, w):
        """
        Moves cursor to next position after the equation.
        """
        if char == "$":
            self.state.current_pos = (
                self.state.current_pos[0]
                + w
                + self.props.pt_size * s.PROPS_GEN["latex_horiz_spacing_multiplier"],
                self.state.current_pos[1],
            )

        elif char == "£":
            self._newline()

    def _process_latex_esc_char(self, char):
        """
        Processes latex equations in the text.
        Returns char_key = None to flag that no char needs
        to be written (since equation is directly blitted).
        """

        # get latex code and a vertical height adjustment
        latex, height_tweak = self._init_latex_process(char)

        # get pygame surf with latex rendererd on it
        latex_surf = self._get_latex_surf(latex, height_tweak)

        if latex_surf is None:
            print("Latex index error!")
            return None

        # scale the surf to correct size
        latex_surf = self._get_scaled_latex_surf(char, latex_surf)

        # get new rect and dimensions
        latex_rect = latex_surf.get_rect()
        w, h = latex_rect.size

        # adjust current_position var to enable blitting it to correct pos
        self._process_latex_position(char, w, h)

        self._blit_latex(latex_surf, latex_rect)

        # leave current_pos in righty pos for next char
        self._move_to_next_position(char, w)

        return None

    def _process_interrupt_esc_char(self, char):
        """
        Processes interrupt-type Esc chars, returns None if ready to move
        to next char or the new processed char to write.
        """

        if char == "p":
            # pause
            pg.time.delay(s.PROPS_GEN["pause_delay"])
            return None

        if char == "w":

            if self.props.instantly:
                # don't pause if instantly flag is true
                return None

            # wait for keypress or quit
            while True:
                response = check_user_event()
                if response in (
                    UserEvent.ESCAPED,
                    UserEvent.WINDOW_CLOSED,
                    UserEvent.KEY_PRESSED,
                ):
                    break

            return None

    def _process_escape_char(self, char):
        """
        Processes Esc chars, returns None if ready to move
        to next char or the new processed char to write.
        """

        if char in s.FORMATTING_ESC_CHARS:
            return self._process_formatting_esc_char(char)

        if char == s.SYMBOL_ESC_CHAR:
            return self._process_symbol_esc_char(char)

        if char in s.LATEX_ESC_CHARS:
            return self._process_latex_esc_char(char)

        if char in s.INTERRUPT_ESC_CHARS:
            return self._process_interrupt_esc_char(char)

        return None

    def _process_linebreaking(self):
        """semi-intelligent line breaking to ensure words
        don't run past edge of text box
        """

        if self.state.current_pos[0] == self.props.origin_pos[0]:
            # at start of newline, so measure next word length from current
            # index in parsed text
            word_length_pixels = self._get_word_length_pixels(
                self.props.parsed_text, self.state.i, self.default_style.scale
            )

        elif (
            self.state.char == " "
            or self.state.char == "."
            and self.state.i + 1 < len(self.props.parsed_text)
            and self.props.parsed_text[self.state.i + 1][1] != " "
        ):
            # not starting a newline and current char is a space or fullstop
            # and next char is not a space, so measure next word length from
            # next index in parsed text
            word_length_pixels = self._get_word_length_pixels(
                self.props.parsed_text, self.state.i + 1, self.default_style.scale
            )

        else:
            # don't need to do any further checking
            return

        # check if next word will fit onto line
        if (
            self.state.current_pos[0] + word_length_pixels
            >= self.props.text_box_left_edge
        ):
            self._newline()

    def _add_space(self):
        """
        Add space unless start of line
        """
        if self.state.current_pos[0] != self.props.origin_pos[0]:
            self.state.current_pos = (
                self.state.current_pos[0] + self.props.word_spacing,
                self.state.current_pos[1],
            )

    def _move_to_next_pos(self):
        """
        next char start at leftmost postion of last char plus the space
        """
        self.state.current_pos = (
            self.state.x_max + self.props.char_spacing,
            self.state.current_pos[1],
        )

    def _write_char(self, char_key):
        """
        Writes char.
        Generator. Yields Flag.USER_QUIT if user quit else None.
        """
        self.state.x_max = 0

        # paths will be from working dict or if not found there, from
        # default dict or None if not found there either.

        # Note: key_val() should substitute key corresp to a question mark
        # for any rogue characters.
        # paths = self.hw_dict.get(char_key,
        #                           self.hw_default_dict.get(char_key, None))

        # might be a way of doing this more elegantly using .get dict method
        if char_key in self.hw_dict:
            paths = self.hw_dict[char_key]
        elif char_key in self.hw_default_dict:
            paths = self.hw_default_dict[char_key]
        else:
            paths = self.hw_default_dict[str(ord(s.PROPS_REC["not_recognised_char"]))]

        # if paths is None:
        #     yield

        for path in paths:
            response = check_user_event()

            if response in (UserEvent.ESCAPED, UserEvent.WINDOW_CLOSED):
                yield Flag.USER_QUIT

            # smooth path
            self.props.bsx.reset()
            self.props.bsy.reset()
            smoothed_path = []

            for data in path:
                x, y = data["pos"]
                # If smooth_level was 0 (i.e. buffer_size = 0) then the smooth
                # method of BufferSmooth immediately returns the value so there
                # should not be too much overhead calling this method
                # even when no smoothing is required. The conditional logic to
                # prevent this was more trouble than it was worth!
                smoothed_x = self.props.bsx.smooth(x)
                smoothed_y = self.props.bsy.smooth(y)
                smoothed_path.append(
                    {"pos": (smoothed_x, smoothed_y), "time": data["time"]}
                )

            dp = self._draw_path(
                smoothed_path,
                (
                    self.state.current_pos[0],
                    self.state.current_pos[1] + self.style.vert_offset,
                ),
                colour=self.style.colour,
                linewidth=self.style.linewidth,
                nib=self.style.nib,
                spray=self.style.spray,
                scale=self.style.scale,
                speed_mult=self.style.speed_mult,
                instantly=self.props.instantly,
                cursor_img=self.props.cursor_img,
            )

            while True:
                try:
                    val = next(dp)
                    yield
                except StopIteration:
                    break

            xm = val
            if xm is not None:
                if xm > self.state.x_max:
                    self.state.x_max = xm

    def _newline(self):
        """
        move to start of next line down
        """
        self.state.current_pos = (
            self.props.origin_pos[0] + s.PROPS_GEN["text_box_margin"],
            self.state.current_pos[1] + self.props.line_spacing,
        )

    def _process_hyphenation(self):
        """
        hyphenation is rather crude; hyphen inserted when next char
        would run over
        """
        if (
            self.state.current_pos[0]
            > self.props.text_box_left_edge - s.PROPS_GEN["text_box_margin"]
        ):

            if (
                self.state.i + 1 < len(self.props.parsed_text)
                and self.props.parsed_text[self.state.i + 1][1] != " "
            ):

                # next character is not a space, hence we are splitting a word,
                # so add a hypen

                char_width, char_height = self.generic_char_size

                hyphen_start_pos = (
                    self.state.current_pos[0]
                    + 0.5 * char_width * self.default_style.scale,
                    self.state.current_pos[1]
                    - 0.5 * char_height * self.default_style.scale,
                )

                hyphen_length = int(
                    (self.props.pt_size / 28) * s.PROPS_GEN["hyphen_length"]
                )
                hyphen_end_pos = (
                    hyphen_start_pos[0] + hyphen_length,
                    hyphen_start_pos[1],
                )
                mod_rect = pg.draw.line(
                    self.surf,
                    self.style.colour,
                    hyphen_start_pos,
                    hyphen_end_pos,
                    self.style.linewidth,
                )
                if self.update_display:
                    pg.display.update(mod_rect)

            if "underline" in self.state.style_set:
                # save position before we move to next line
                self.state.underline_end_pos = (
                    self.state.current_pos[0],
                    self.state.current_pos[1] + s.PROPS_GEN["underline_offset"],
                )

            self._newline()

    def _process_underlining(self):
        """
        Handles underlining of text. This just appears and is currently not
        animated.
        """
        if self.state.underline_end_pos is None:
            self.state.underline_end_pos = (
                self.state.current_pos[0],
                self.state.current_pos[1] + s.PROPS_GEN["underline_offset"],
            )

        mod_rect = pg.draw.line(
            self.surf,
            self.style.colour,
            self.state.underline_start_pos,
            self.state.underline_end_pos,
            self.style.linewidth,
        )

        if self.update_display:
            pg.display.update(mod_rect)

    def char_okay(self, char):
        """
        Returns True if path data exists for char else False.
        Note: not a private method, since user may want to check a char.
        """
        if char in s.SYMBOL_CHARS:
            # ok
            return True

        if len(char) > 1:
            # not okay (only _chars are longer than 1 char)
            return False

        if ord(char) in self.hw_dict:
            # ok
            return True

        # other possibilities --> not okay
        return False

    # consider moving these params into the __init__
    def write_text(
        self,
        text,
        update_display=None,
        text_rect=None,
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

        r"""
        Method to animate the writing of text to surf.

        params:
        ------
        text: str
            text to be handwritten

        update_displate: bool
            if true, the calling code (e.g. handwriter.py) is passing the
            screen as the surface to be written on, and so this requires
            pg.display.update() calls in this code after blits to show those
            blits.
            None --> default used
        text_box_rect: (x,y, w, h) or equivalent pygame rect specifying the
        bounding rect for the written text **RELATIVE** to the passed surf.

        colour: int tuple (r,g,b,a)
            default colour for handwritten text
            can be overridden with \col - see below

        linewidth: int
            default linewidth in pixels of written text
            can be overridden with \bold - see below

        nib: dict of nib parameters for calligraphy style writing
            keys:
                "width" is nib width in pixels
                "angle "is nib angle in degrees measured clockwise from horiz
            nib={"width":5, "angle":45} looks good.

        spray: dict of spray parameters for spray-paint writing
            keys:
                "width" is spray width in pixels
                "col" is spray RGBA colour (alpha will be handled properly)
                "aspect_ratio" width:height of spray, e.g. a value of 2
                    means height will be half the width
                "angle" spray angle in degrees measured clockwise from horiz,
                    only makes sense if aspect ratio is not 1.

        pt_size: int
            default pt_size for handwritten text
            can be overridden with \bigger, \smaller - see below

        char_spacing: int
            default spacing between written chars in pixels

        line_spacing: int
            default spacing between lines of written text in pixels

        speed_mult: float
            default writing speed (1 = speed at which handwriting was recorded)

        instantly: Bool
            if true, text appears instantly

        cursor: string or pygame surface
            Either name of one of the built-in cursor types or pygame surface
            holding custom cursor image. NB:topleft of image is where ink comes
            from. If None, no cursor is shown.

        cursor_sf: float
            scale factor for cursor image, e.g. if cursor_sf=2, then cursor
            image will be doubled in size.

        num_tabs: int
            number of tab stops across text box

        hyphenation: Bool
            if true, a crude form of hyphenation is employed if word runs past
            edge of text box
            else words are not split, but can very leave ragged edge

        surf_bg_col: int tuple (r,g,b,a)
            surf background colour, default is none

        surf_border_width: int
            surf border width in pixels (0 or None --> no border)
            default is none

        surf_border_col: int tuple (r,g,b,a)
            surf border colour
            default is none

        text_rect_bg_col: int tuple (r,g,b,a)
            text_rect background colour, default is none

        text_rect_border_width: int
            text_rect border width in pixels (0 or None --> no border)
            default is none

        text_rect_border_col: int tuple (r,g,b,a)
            text_rect border colour
            default is none


        Styles (effects)
        ---------------
        \col{text} colour text
        where col is a colour string (see common_colours.py)
        e.g. \red{text}

        \bold{text} make text bold

        \underline{text} underline text

        \super{text} superscript text
        \sub{text} subscript text

        \up{text} move text up
        \down{text} move text down

        \bigger{text} make text bigger
        \smaller{text} make text smaller

        \doublespeed{text} write text doublespeed
        \halfspeed{text} write text halfspeed


        Formatting escape chars
        -----------------------
        \n newline
        \t tab


        Flow control escape chars
        -------------------------
        \p pause 0.5 sec
        \w wait for user to press key (or quit)


        Symbols delimiters
        -------------------
        Use backtick (not single quote!) to embed symbol, like in markdown:
        `symbol_name`

            built_in symbols:

            `left`  left arrow
            `right` right arrow
            `up` up arrow
            `down` down arrow

            `happy` happy emojie
            `sad` sad emojie
            `excited` excited emojie
            `bored` bored emojie
            `confused` confused emojie


        Equations
        ---------
        ${tex} insert inline latex equation
        £{tex} insert newline latex equation


        Examples of text param
        ----------------------
        Note use of r (raw) to allow escape chars in string and \ to allow
        string to extend over line

        text = r"This is a demo of handwriter . py. "\
        r"This is \underline{underlined. }"\
        r"\bold{This is bold text}. "\
        r"\red{This is red text}. "\
        r"\bold{\red{This is bold red text showing nesting of styles! }}"\
        r"\nSuperscript E =mc\super{2}.  "\
        r"\bigger{\bigger{BIGGER}} text. \n"\
        r"\t\green{Text}\t\yellow{in}\t\maroon{columns}\t\cyan{with tabs} \n"\
        r"\doublespeed{Faster writing}. "\
        r"\blue{A 1 second pause..... \p\p ... finished! }"\
        r"An inline latex eqn in magenta \magenta{$a x^2 + b x + c = 0$}."\
        r"A centred newline latext equation "\
        r"\bigger{\gold{£F(x) = \int^a_b \frac{1}{3}x^3£}}"\
        r"Emojies and arrows: Happy face \r \bigger{\green{#happy#}}\n"\
        r"Things getting you \d \bigger{\blue{#sad#}} ?\n"\
        r"Left arrow #left#, down arrow #down#"

        """
        # first check for illegal Esc tokens in text
        i = legal_token_check.get_illegal_index(text)
        if i is not None:
            raise Exception(f"Unrecognised Esc token at index position {i} in text!")
        # TODO could show text with error position marked

        self.update_display = (
            s.PROPS_GEN["update_display"] if update_display is None else update_display
        )

        # Put attributes into containers to keep track of them.

        # properties ---------------------------------------------------------
        self.props = Container()
        if text_rect is None:
            # centre text rect on surf with uniform gap all around
            surf_rect = self.surf.get_rect()
            b = s.PROPS_GEN["text_box_border"]
            self.props.rect = surf_rect.inflate((-b, -b))
        else:
            self.props.rect = pg.Rect(text_rect)
        self.props.origin_pos = self.props.rect.topleft  # rect is rel to surf
        self.props.text_box_width = self.props.rect.width
        self.props.text_box_height = self.props.rect.height
        self.props.num_tabs = s.PROPS_GEN["num_tabs"] if num_tabs is None else num_tabs
        self.props.tab_spacing = self.props.text_box_width // self.props.num_tabs
        self.props.text_box_left_edge = (
            self.props.origin_pos[0] + self.props.text_box_width
        )
        self.props.pt_size = pt_size or s.PROPS_GEN["display_pt_size"]
        self.props.super_offset = s.PROPS_GEN["super_offset_sf"] * self.props.pt_size
        self.props.sub_offset = s.PROPS_GEN["sub_offset_sf"] * self.props.pt_size
        self.props.up_offset = s.PROPS_GEN["up_offset_sf"] * self.props.pt_size
        self.props.down_offset = s.PROPS_GEN["down_offset_sf"] * self.props.pt_size
        self.props.char_spacing = (
            s.PROPS_GEN["char_spacing"] if char_spacing is None else char_spacing
        )
        self.props.word_spacing = (
            s.PROPS_GEN["word_spacing"] if word_spacing is None else word_spacing
        )
        self.props.line_spacing = (
            self.props.pt_size * 1.5 if line_spacing is None else line_spacing
        )
        # the next two can get populated by preprocess_text()!
        self.props.latex_inline_list = None
        self.props.latex_newline_list = None
        self.props.symbol_list = None
        self.props.parsed_text = parse(
            self._preprocess_text(text), style_tokens.STYLE_TOKENS
        )
        if self.props.parsed_text is None:
            error_msg = f"""Error parsing text. Check that all curly brackets
            are paired and that all Escaped tokens are legal,
            especially those starting with {s.ESC_CHARS}"""
            raise Exception(error_msg)
        self.props.hyphenation = hyphenation
        self.props.instantly = instantly

        # I had to change alpha of text_rect_bg_col to 255 to make latex equations
        # work, but I think there was a good reason why I had put it to zero ...?
        # self.props.text_rect_bg_col = (0,0,0,0) if text_rect_bg_col is None else text_rect_bg_col
        self.props.text_rect_bg_col = (
            (0, 0, 0, 255) if text_rect_bg_col is None else text_rect_bg_col
        )
        if cursor is None:
            self.props.cursor_img = None
        else:
            if isinstance(cursor, pg.Surface):
                self.props.cursor_img = cursor  # use passed cursor img
            else:
                try:
                    self.props.cursor_img = self.cursors[cursor]
                except:
                    # could throw KeyError if key doesn't exist
                    # or TypeError if non-hashable key
                    self.props.cursor_img = self.cursors[s.PROPS_GEN["default_cursor"]]
            if cursor_sf is not None:
                self.props.cursor_img = pg.transform.rotozoom(
                    self.props.cursor_img, 0, cursor_sf
                )
        # style---------------------------------------------------------------
        self.default_style = Container()
        self.default_style.colour = colour or s.PROPS_GEN["colour"]
        self.default_style.linewidth = linewidth or s.PROPS_GEN["linewidth"]
        self.default_style.nib = nib  # default value is None
        self.default_style.spray = spray  # default value is None
        if spray is not None:
            self._customise_spray(spray)
        # scale factor depends on pt size that path was saved as in recorder.py
        self.default_style.scale = self.props.pt_size / s.PROPS_REC["save_pt_size"]
        self.default_style.speed_mult = (
            speed_mult * s.PROPS_GEN["speed_mult"]
            if speed_mult is not None
            else s.PROPS_GEN["speed_mult"]
        )
        self.default_style.vert_offset = 0

        # state---------------------------------------------------------------
        self.state = Container()
        # move down and to right of top left of bounding rect to start first
        # char
        self.state.current_pos = (
            self.props.origin_pos[0] + s.PROPS_GEN["text_box_margin"],
            self.props.origin_pos[1] + self.props.line_spacing,
        )

        self.state.skip_next_char = False
        self.state.latex_inline_count = 0
        self.state.latex_newline_count = 0
        self.state.symbol_count = 0
        self.state.underline_start_pos = None
        self.state.underline_end_pos = None
        self.state.x_max = None
        self.state.i = None
        self.state.style_set = None
        self.state.char = None

        self.props.char_spacing *= self.default_style.scale
        self.props.word_spacing *= self.default_style.scale

        # any smooth_value not in 0-9 inclusive will default to default_smooth_level
        buffer_size = s.PROPS_REC["smooth_levels"].get(
            smooth_level, s.PROPS_REC["default_smooth_level"]
        )
        # print("buffer size = ", buffer_size) # debug
        self.props.bsx = BufferSmooth(buffer_size=buffer_size)
        self.props.bsy = BufferSmooth(buffer_size=buffer_size)

        # Backgrounds and borders
        # Note that pygame does not allow screen (display) to be filled
        # with transparent colour, i.e. alpha channel is ignored.
        # This creates a problem if calling code has passed the screen as their
        # destination surface!
        # Also, pg.draw.rect etc also ignore the alpha channel.
        # A workaround is to create a new surface of the same size with
        # the pg.SRCALPHA flag set to accept alpha channel. Then fill (or draw
        # rect onto) that and then blit that onto the screen surface.
        # Luckily this only needs to be done once at the start.

        if surf_bg_col is not None:
            temp_surf = pg.Surface(self.surf.get_size(), pg.SRCALPHA)
            temp_surf.fill(surf_bg_col)
            self.surf.blit(temp_surf, (0, 0))
        if surf_border_width is not None and surf_border_col is not None:
            temp_surf = pg.Surface(self.surf.get_size(), pg.SRCALPHA)
            pg.draw.rect(
                temp_surf, surf_border_col, self.surf.get_rect(), surf_border_width
            )
            self.surf.blit(temp_surf, (0, 0))
        if text_rect_bg_col is not None:
            temp_surf = pg.Surface(self.props.rect.size, pg.SRCALPHA)
            temp_surf.fill(text_rect_bg_col)
            self.surf.blit(temp_surf, self.props.origin_pos)
        if text_rect_border_width is not None and text_rect_border_col is not None:
            temp_surf = pg.Surface(self.surf.get_size(), pg.SRCALPHA)
            pg.draw.rect(
                temp_surf, text_rect_border_col, self.props.rect, text_rect_border_width
            )
            self.surf.blit(temp_surf, (0, 0))
        if self.update_display:
            pg.display.flip()

        def write_text_gen():
            """
            A generator that writes the text char by char.

            Each char is written path by path, where a path is a continous line
            without pen leaving paper.
            Each path is drawn as a series of straight line segments, with a
            delay between each, as recorded during training.
            This is implmeneted in the form of generators to allow control to
            be passed back to the calling code during the delays to allow
            parallel animations etc.

            Yields Flag.USER_QUIT if user quit, Flag.OVERFLOW if the text
            overflowed the text rec.

            The yield is implemented in a manner to allow a send back to the
            generator to change parmeters on the fly. Currently this is only
            used for the speed multiplier.
            """

            # print(f"{self.props.parsed_text}") # debug
            # loop through text................................................
            for self.state.i, (self.state.style_set, self.state.char) in enumerate(
                self.props.parsed_text
            ):

                # set style to default
                self.style = deepcopy(self.default_style)

                # escape chars need to be skipped
                if self.state.skip_next_char:
                    self.state.skip_next_char = False
                    continue

                # handwriting style-------------------------------------------
                self._process_style()

                # linebreaking------------------------------------------------
                # previously after processing of escape chars
                if not self.props.hyphenation:
                    self._process_linebreaking()

                self.state.underline_end_pos = None

                # spaces-------------------------------------------------------
                # previously after processing of escape chars
                if self.state.char == " ":
                    self._add_space()
                    continue

                # escape chars------------------------------------------------
                if self.state.char == "\\":

                    try:
                        next_char = self.props.parsed_text[self.state.i + 1][1]
                    except IndexError:
                        break

                    self.state.skip_next_char = True

                    char_key = self._process_escape_char(next_char)

                    if char_key is None:
                        continue

                else:
                    # not an escape char
                    char_key = get_char_key(self.state.char)

                # char_key is either unicode for a "regular" char
                # or the symbol name

                # handwrite char-----------------------------------------------
                wc = self._write_char(char_key)  # generator
                while True:

                    try:
                        val = next(wc)

                    except StopIteration:
                        break

                    if self.state.current_pos[1] > self.props.text_box_height:
                        yield Flag.OVERFLOW

                    elif val is Flag.USER_QUIT:
                        yield Flag.USER_QUIT

                    else:
                        received_data = yield self.state.current_pos

                        if received_data is not None:
                            self.default_style.speed_mult *= received_data

                # move to next position----------------------------------------
                self._move_to_next_pos()

                # hyphenation--------------------------------------------------
                if self.props.hyphenation:
                    self._process_hyphenation()

                # underlining-------------------------------------------------
                if "underline" in self.state.style_set:
                    self._process_underlining()

            if self.props.instantly and self.update_display:
                pg.display.flip()

            # end of inner func------------------------------------------------

        # OUTER FUNC STARTS HERE ----------------------------------------------
        # Return a generator which calling code can use frame by frame
        # note that this generator will yield Flag.USER_QUIT if user has exited
        # and Flag.OVERFLOW if the text has overflowed.
        # Up to calling code to decide how to handle these cases.
        # Calling code can also use "send" to send data back to the yield
        # to change the speed multiplier

        wtg = write_text_gen()

        if self.props.instantly:
            while True:
                try:
                    val = next(wtg)
                    if val is Flag.USER_QUIT or val is Flag.OVERFLOW:
                        # update display evn on break, else nothing shows
                        if self.update_display:
                            pg.display.flip()
                        break
                except StopIteration:
                    val = None
                    break
            return oneshot_generator(val)

        return wtg  # generator
