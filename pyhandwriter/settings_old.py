# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 13:11:59 2021

@author: jwgti
"""

import os
import string
from .colours import col

FORMATTING_ESC_CHARS = ("n", "t")

INTERRUPT_ESC_CHARS = ("p", "w")

ESC_CHARS = list(FORMATTING_ESC_CHARS) + list(INTERRUPT_ESC_CHARS)

#TODO these should not be called escape chars since no preceding \ required
# Rename to LATEX_INSERT_CHARS and SYMBOL_INSERT_CHARS??
LATEX_ESC_CHARS = ("$", "£")

SYMBOL_ESC_CHAR = "`"  # Backtick, as used in markdown

COMMON_CHARS = string.ascii_letters + string.digits + string.punctuation

# built-in cursor filenames
path = os.path.join(os.path.dirname(__file__), "assets")
quill_dark_cursor_fname = os.path.join(path, "quill_dark.png")
quill_light_cursor_fname = os.path.join(path, "quill_light.png")
pencil_cursor_fname = os.path.join(path, "pencil_cursor.png")
crosshair_cursor_fname = os.path.join(path, "crosshair_cursor.png")
circle_cursor_fname = os.path.join(path, "circle_cursor.png")
square_cursor_fname = os.path.join(path, "square_cursor.png")
arrow_cursor_fname = os.path.join(path, "arrow_cursor.png")
spray_can_cursor_fname = os.path.join(path, "spraycan.png")

CURSORS = {
    "pencil": pencil_cursor_fname,
    "quill_dark": quill_dark_cursor_fname,
    "quill_light": quill_light_cursor_fname,
    "crosshair": crosshair_cursor_fname,
    "circle": circle_cursor_fname,
    "square": square_cursor_fname,
    "arrow": arrow_cursor_fname,
    "spray_can": spray_can_cursor_fname,
}

# properties for handwriter_gen
PROPS_GEN = {
    "fname_separator": "#",
    "default_hw_font": "hw_segoescript",
    "hw_font_folder": "hw_fonts",  # assumed to be in same folder as handwriter_gen.py etc
    "hw_symbol_folder": "hw_symbols",  # assumed to be in same folder as handwriter_gen.py etc
    "hw_symbol_fname": "hw_symbol",
    "colour": col("WHITE"),
    "display_pt_size": 30,
    "linewidth": 1,
    "speed_mult": 5.0,
    "smooth": 1,
    "char_spacing": 0,
    "word_spacing": 9,
    "scale": 1.0,
    "text_box_border": 50,  # default gap between text box within surface
    "text_box_margin": 20,  # right hand margin bufffer zone
    "super_size_sf": 0.55,  # scale factor for superscripts
    "sub_size_sf": 0.55,  # scale factor for subscripts
    "super_offset_sf": -0.4,  # scale factor for superscript offset (rel to point size); up is negative
    "sub_offset_sf": 0.2,  # scale factor for subscript offset (rel to point size); down is positive
    "up_offset_sf": -0.2,
    "down_offset_sf": 0.2,
    "underline_offset": 5,  # down is positive
    "bold_linewidth_sf": 4,
    "change_colour_pause": 5000,
    "pause_delay": 500,
    "num_tabs": 6,
    "latex_inline_height_scaling": 1.2,
    "latex_newline_height_scaling": 1.5,
    "latex_inline_vert_offset_multiplier": 0.15,
    "latex_full_line_scaling": 0.9,
    "latex_horiz_spacing_multiplier": 0.2,
    "latex_newline_vert_padding": 10,
    "scale_multipler": 1.5,  # for "bigger", "smaller" styles,
    "default_cursor_type": "pencil",
    "sub_for_missing_char": "?",
    "hyphen_length": 15,
    "default_cursor": "pencil",
    # default val for kw arg in write_text; true=> screen passed so need to
    # update entire display rather than modified rect
    "update_display": True,
}


# properties for recorder.py
PROPS_REC = {
    "help_text0": "LMB hold=record, 0-9=smooth level, S=Save, A=Save As, N=Next, P=Previous, Del=delete",
    "help_text1": "Space=preview, Alt=toggle trace/prompt, B=toggle Box on/noff, Esc/close window=Quit",
    "trace_title_text": "RECORDING: TRACE CHARACTER IN BOX",
    "prompt_title_text": "RECORDING: WRITE PROMPT CHARACTER IN BOX",
    "title_offset": (0, 20),
    "prompt_font": "segoescript",
    "pt_size": 200,  # 200
    "save_pt_size": 20,
    "save_as_prompt": "Enter filename : ",
    "msg_pt_size": 24,
    "msg_offset": (0, 100),
    "msg_height": 30,
    "save_as_offset": (100, -50),
    "fps": 60,
    "help_pt_size": 18,
    "help_offset0": (0, -100),
    "help_offset1": (0, -70),
    "box_horiz_offset": 0,
    "box_vert_offset": 100,
    "title_pt_size": 24,
    "bg_col": col("BLACK"),
    "replay_offset": 200,
    "replay_col": col("GREEN"),
    "replay_scale": 10,
    "replay_speed_mult": 1,
    "replay_linewidth": 5,
    "sample_col": col("WHITE"),
    "prompt_horiz_offset": 50,
    "box_col": col("WHITE"),
    "trace_col": col("BLUE"),
    "trace_linewidth": 5,
    "ruler_col": col("DARKGRAY"),
    "cursor_col": col("PINK"),
    "cursor_radius": 5,
    "cursor_linewidth": 0,  # 0 = filled in cursor
    "text_input_font": "consolas",
    "text_input_size": 24,
    "text_input_max_len": 20,
    "text_input_col": col("WHITE"),
    "text_input_x": 100,
    "text_input_y_offset": 50,
    "pause_ms": 1500,
    "invalid_text": "Invalid filename!",
    "default_smooth_level": 0,
    "smooth_pt_size": 16,
    "smooth_offset": (0, -50),
    "smooth_levels": {
        0: 0,
        1: 4,
        2: 8,
        3: 12,
        4: 16,
        5: 20,
        6: 24,
        7: 28,
        8: 32,
        9: 36,
    },
    "not_recognised_char": "?",
}
