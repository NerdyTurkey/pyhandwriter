# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 07:13:56 2021

@author: NerdyTurkey
"""
from .handwriter_gen import HandWriterGen
from .enums import Flag


class HandWriter:
    r""" 
    Animates the writing of text.        
    An interface for HandWriterGen.
    
    params:
    ------    
        
    text: str
        text to be handwritten
    
    update_displate: bool
        if true, the calling code (e.g. handwriter.py) is passing the
        screen as the surface to be written on, and so this requires 
        pg.display.update() calls in this code after blits to show those 
        blits.
    
    text_rect: (x,y, w, h) or equivalent pygame rect specifying the 
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

    def __init__(self, screen, hw_font=None):
        self.screen = screen
        self.hw = HandWriterGen(self.screen, hw_font)

    def write_text(
        self,
        text,
        update_display=None,
        text_rect=None,
        colour=None,
        linewidth=None,
        smooth_level=None,
        pt_size=None,
        char_spacing=None,
        word_spacing=None,
        line_spacing=None,
        nib=None,
        spray=None,
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
        quit_on_overflow=True,
    ):

        # get generator
        self.g = self.hw.write_text(
            text,
            update_display=update_display,
            text_rect=text_rect,
            colour=colour,
            linewidth=linewidth,
            smooth_level=smooth_level,
            nib=nib,
            spray=spray,
            pt_size=pt_size,
            char_spacing=char_spacing,
            word_spacing=word_spacing,
            line_spacing=line_spacing,
            speed_mult=speed_mult,
            instantly=instantly,
            cursor=cursor,
            cursor_sf=cursor_sf,
            num_tabs=num_tabs,
            hyphenation=hyphenation,
            surf_bg_col=surf_bg_col,
            surf_border_width=surf_border_width,
            surf_border_col=surf_border_col,
            text_rect_bg_col=text_rect_bg_col,
            text_rect_border_width=text_rect_border_width,
            text_rect_border_col=text_rect_border_col,
        )

        while True:
            try:
                val = next(self.g)
            except StopIteration:
                return Flag.FINISHED
            else:
                if val is Flag.USER_QUIT or (val is Flag.OVERFLOW and quit_on_overflow):
                    return val
