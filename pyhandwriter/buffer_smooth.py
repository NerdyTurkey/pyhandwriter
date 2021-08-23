# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 14:36:08 2021

@author: NerdyTurkey
"""


class BufferSmooth:
    """
    Smooths a stream of data in real time.
    Each call to smooth with a data point adds that point to a buffer.
    If the buffer size is reached, the first in is ejected.
    The return value is the mean of the buffer.
    """

    def __init__(self, buffer_size=None, weighted=True):
        self.buffer_size = 10 if buffer_size is None else buffer_size
        self.buffer = []
        self.weighted = weighted

    def smooth(self, val):
        if self.buffer_size <= 0:
            return val
        self.buffer.append(val)
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)
        if self.weighted:
            # weighted sum, most recent weighted higher
            weights = range(1, len(self.buffer) + 1)
            return sum(
                [weight * val for weight, val in zip(weights, self.buffer)]
            ) / sum(weights)
        # else equal weights
        return sum(self.buffer) / len(self.buffer)

    def reset(self, buffer_size=None):
        if buffer_size is not None:
            self.buffer_size = buffer_size
        self.buffer = []
