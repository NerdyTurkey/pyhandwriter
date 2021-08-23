# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 07:07:32 2020

@author: NerdyTurkey
"""
from .colours import col_dict

# Note that instead of. eg. "\\bold", could have used r"\bold"

STYLE_TOKENS = {
    "bold": "\\bold",
    "underline": "\\underline",
    "sub": "\\sub",
    "super": "\\super",
    "doublespeed": "\\doublespeed",
    "halfspeed": "\\halfspeed",
    "bigger": "\\bigger",
    "smaller": "\\smaller",
    "up": "\\up",
    "down": "\\down",
}

for col in col_dict:
    STYLE_TOKENS[col.lower()] = "\\" + col.lower()
