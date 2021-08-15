# -*- coding: utf-8 -*-
"""
Created on Sat May  2 09:24:14 2020

@author: jt
"""

"""
Copyright 2017, Silas Gyger, silasgyger@gmail.com, All rights reserved.

Borrowed from https://github.com/Nearoo/pygame-text-input under the MIT license.
with jt additions to take advantage of pygame2 features
"""

# import os.path

import pygame as pg
import pygame.freetype

# import pygame.locals as pl

IS_PYGAME2 = pg.get_sdl_version() > (2, 0, 0)


def get_font(font_name, size=None):
    """
    Converts a font_name (string) to a pygame font object
    """

    if size is None:
        size = 18

    font_object = pg.freetype.SysFont("consolas", size)  # default value

    # First check if font_name is a system font
    if font_name in pg.freetype.get_fonts():
        return pg.freetype.SysFont(font_name, size)

    else:
        # Not a system font, so try loading it

        try:
            return pg.freetype.Font(font_name, size)

        except:
            print("font not found - default will be substituted")
            pass

    return font_object


# ==============================================================================


class TextInput:
    """
    This class lets the user input a piece of text, e.g. a name or a message.
    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, home and end work as well.
    Adapted by JT to search more intelligently for font and to allow
    alpha channel on text_color (ie.g. semi-transparent text)
    """

    def __init__(
        self,
        initial_string=None,
        font_name=None,
        text_size=None,
        text_color=None,
        cursor_color=None,
        cursor_blink_ms=None,
        repeat_keys_initial_ms=None,
        repeat_keys_interval_ms=None,
        max_string_length=None,
        cursor_offset=None,
    ):
        """
        :param initial_string: Initial text to be displayed
        :param font_family: name or list of names for font (see pygame.font.match_font for precise format)
        :param text_size:  Size of font in pixels
        :param text_color: Color of text (duh)
        :param cursor_color: Color of cursor
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :param repeat_keys_interval_ms: Interval between key press repetition when held
        :param max_string_length: Allowed length of text
        """

        # Text related va5rs:
        self.text_color = (255, 255, 255) if text_color is None else text_color
        self.text_size = 18 if text_size is None else text_size
        self.max_string_length = -1 if max_string_length is None else max_string_length
        self.input_string = (
            "" if initial_string is None else initial_string
        )  # Inputted text
        font_name = "consolas" if font_name is None else font_name
        self.font_object = get_font(font_name, size=self.text_size)

        # Text-surface will be created during the first update call:
        self.surface = pg.Surface((1, 1), pg.SRCALPHA)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = (
            {}
        )  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = (
            400 if repeat_keys_initial_ms is None else repeat_keys_initial_ms
        )
        self.keyrepeat_interval_ms = (
            35 if repeat_keys_interval_ms is None else repeat_keys_interval_ms
        )

        # Things cursor:
        self.cursor_offset = 5 if cursor_offset is None else cursor_offset  # pixels
        cursor_color = (255, 255, 255) if cursor_color is None else cursor_color
        self.cursor_surface = pg.Surface((int(self.text_size / 20 + 1), self.text_size))
        self.cursor_width, self.cursor_height = self.cursor_surface.get_size()
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(self.input_string)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_blink_ms ms
        self.cursor_blink_ms = 250 if cursor_blink_ms is None else cursor_blink_ms
        self.cursor_ms_counter = 0

        self.clock = pg.time.Clock()

    def update(self, events):
        for event in events:
            char = ""
            if event.type == pg.KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if event.key not in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pg.K_BACKSPACE:
                    self.input_string = (
                        self.input_string[: max(self.cursor_position - 1, 0)]
                        + self.input_string[self.cursor_position :]
                    )

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pg.K_DELETE:
                    self.input_string = (
                        self.input_string[: self.cursor_position]
                        + self.input_string[self.cursor_position + 1 :]
                    )

                elif event.key == pg.K_RETURN:
                    return True

                elif event.key == pg.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(
                        self.cursor_position + 1, len(self.input_string)
                    )

                elif event.key == pg.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pg.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pg.K_HOME:
                    self.cursor_position = 0

                elif not IS_PYGAME2 and (
                    len(self.input_string) < self.max_string_length
                    or self.max_string_length == -1
                ):
                    char = event.unicode
                    self.input_string = (
                        self.input_string[: self.cursor_position]
                        + char
                        + self.input_string[self.cursor_position :]
                    )
                    self.cursor_position += len(char)  # Some are empty, e.g. K_UP

            elif event.type == pg.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

            elif (
                IS_PYGAME2
                and event.type == pg.TEXTINPUT
                and (
                    len(self.input_string) < self.max_string_length
                    or self.max_string_length == -1
                )
            ):
                char = event.text
                self.input_string = (
                    self.input_string[: self.cursor_position]
                    + char
                    + self.input_string[self.cursor_position :]
                )
                self.cursor_position += len(char)  # Some are empty, e.g. K_UP

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = (
                    self.keyrepeat_intial_interval_ms - self.keyrepeat_interval_ms
                )

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pg.event.post(
                    pg.event.Event(pg.KEYDOWN, key=event_key, unicode=event_unicode)
                )

        # Re-render text surface:
        # JT mod to pad out text surface to allow cursor to be offset from last char
        temp_surface, _ = self.font_object.render(
            self.input_string, fgcolor=self.text_color, bgcolor=None
        )  # transparent background
        w, h = temp_surface.get_size()
        self.surface = pg.Surface(
            (w + self.cursor_offset + self.cursor_width, h), pg.SRCALPHA
        )
        self.surface.blit(temp_surface, (0, 0))
        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_blink_ms:
            self.cursor_ms_counter %= self.cursor_blink_ms
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_x_pos = self.font_object.get_rect(
                self.input_string[: self.cursor_position]
            ).width
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0:
                cursor_x_pos -= self.cursor_surface.get_width()
            self.surface.blit(
                self.cursor_surface, (cursor_x_pos + self.cursor_offset, 0)
            )

        self.clock.tick()
        return False

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0


if __name__ == "__main__":
    pg.init()
    # Create TextInput-object
    textinput = TextInput(
        text_size=28, text_color=(0, 0, 255, 255), max_string_length=10
    )
    # textinput = TextInput()
    # textinput = TextInput(font_name = 'colonna', text_size=40, text_color=(0,0,255,255), max_string_length=20)

    screen = pg.display.set_mode((900, 600))
    # set_foreground_window(window_name = 'pygame window')
    clock = pg.time.Clock()

    while True:
        # screen.fill((225, 255, 255))
        screen.fill((0, 0, 0))
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()

        # Feed it with events every frame
        ret_val = textinput.update(events)
        if ret_val:
            text_entered = textinput.get_text()
            break
        # Blit its surface onto the screen
        screen.blit(textinput.get_surface(), (400, 200))

        pg.display.update()
        clock.tick(30)

    print("text entered = ", text_entered)
    pg.quit()
