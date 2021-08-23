# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 12:32:19 2020

@author: NerdyTurkey
"""

"""

Note: matplotlib and PIL are not in standard library

If these cannot be imported, we want the package still to operate but latex
equations won't be rendered.

To gracefully handle the failed imports:

log the failed imports using a config scrip to share info between modules and
then define a dummy latex_to_img function which will raise an exception when
called which  will be caught by try/except block in handwriter_gen.

"""


import warnings
from . import config

import_failed = False

try:
    import matplotlib.pyplot as plt

    # import non_existant_module # for testing only
except ImportError:
    import_failed = True
    config.failed_imports.append("matplotlib")
    warnings.warn("matplotlib could not be imported - latex equations will not work")

try:
    from PIL import Image, ImageChops

    # import non_existant_module # for testing only
except ImportError:
    import_failed = True
    config.failed_imports.append("PIL")
    warnings.warn("PIL could not be imported - latex equations will not work")

if import_failed:
    # at least one fatal ImportError
    def latex_to_img():
        """dummmy function definition designed to cause error which will
        be trapped gracefully later"""
        pass


else:
    # imports all fine
    import io
    from .colours import col

    MIN_PT_SIZE = 2
    MAX_PT_SIZE = 1000
    BUFFER = 50
    MARGIN = 5

    def convert_col(col):
        """
        Converts colour tuple, col,  with component channels in range 0-255
        to a colour tuple with component channels in range 0-1 as needed by
        matplotlib
        """
        return [x / 255 for x in col]

    def latex_to_img(tex, pt_size=60, text_col=col("WHITE"), bg_col=col("BLUE")):
        """
        Returns an image file containing rendered tex.
        Params are self-obvious.

        The tex is first rendererd on a matplotlib plot at pt_size, the text
        bounding box is measured and then the pt_size is adjusted for a second
        pass to try and fill the width of the plot with the equation for optimal
        resolution (I couldn't think of a way to do this a-priori).

        The figure is then 'saved' as png using io.BytesIO().
        The png is then loaded with PIL and cropped to the bounding box of the text.
        """

        if not (MIN_PT_SIZE <= pt_size <= MAX_PT_SIZE):
            print("pt size error!")
            return None
        buf = io.BytesIO()  # for temp save of plt fig
        fig = plt.figure()
        ax = plt.gca()
        renderer = fig.canvas.get_renderer()
        axes_bb = ax.get_window_extent(renderer=renderer)  # axes bounding box
        axes_width = axes_bb.width

        plt.rcParams["text.color"] = convert_col(text_col)
        plt.rcParams["axes.facecolor"] = convert_col(bg_col)
        plt.rcParams["savefig.facecolor"] = convert_col(bg_col)
        plt.rc("text", usetex=True)
        plt.rc("font", family="serif")
        plt.axis("off")

        text = plt.text(0.0, 0.5, f"${tex}$", size=pt_size)
        text_bb = text.get_window_extent(renderer=renderer)
        text_width = text_bb.width

        # scale pt_size to try and get equation to fill width of plot
        pt_size *= max(1, int(0.2 * axes_width / text_width))
        plt.close(fig)

        # and repeat with new pt_size

        if not (MIN_PT_SIZE <= pt_size <= MAX_PT_SIZE):
            print("pt size error!")
            return None
        buf = io.BytesIO()  # for temp save of plt fig
        fig = plt.figure()
        ax = plt.gca()
        renderer = fig.canvas.get_renderer()
        axes_bb = ax.get_window_extent(renderer=renderer)
        axes_width = axes_bb.width

        plt.rcParams["text.color"] = convert_col(text_col)
        plt.rcParams["axes.facecolor"] = convert_col(bg_col)
        plt.rcParams["savefig.facecolor"] = convert_col(bg_col)
        plt.rc("text", usetex=True)
        plt.rc("font", family="serif")
        plt.axis("off")

        text = plt.text(0.0, 0.5, f"${tex}$", size=pt_size)
        plt.ioff()
        plt.savefig(buf, format="png")
        plt.close(fig)

        # Crop the image to the size of the rendered tex-----------

        # subtract bg col, so regions outside of text will be zeroed
        im = Image.open(buf)
        # im.show() # should be commented out
        bg = Image.new(im.mode, im.size, bg_col)
        diff = ImageChops.difference(im.convert("RGB"), bg.convert("RGB"))
        diff = ImageChops.add(diff, diff, 2.0, -100)  # not needed???

        # diff.show() # should be commented out
        # get bounding box of non-zero regions in image
        bbox = diff.getbbox()

        # add a small margin
        bbox = (bbox[0] - MARGIN, bbox[1] - MARGIN, bbox[2] + MARGIN, bbox[3] + MARGIN)

        # return cropped image
        return im.crop(bbox)


def main():
    # example usage
    latex_to_img(
        r"\frac{\cos(x)}{y^2+\exp(\pi)}", text_col=col("YELLOW"), bg_col=col("MAGENTA")
    ).save("img.png")
    # latex_to_img(r'x=\frac{-b\pm\sqrt{b^2-4 a c}}{2 a}', text_col=col("BLACK"), bg_col=col("MAGENTA")).save('img.png')
    # latex_to_img(r'a', text_col=col("BLACK"), bg_col=col("MAGENTA")).save('img.png')


if __name__ == "__main__":
    main()
