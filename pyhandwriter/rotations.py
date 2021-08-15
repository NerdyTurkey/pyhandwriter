# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:38:18 2021

@author: jwgti
"""

import pygame as pg


def get_rotated_images(img, rotation_angles, clockwise=True):
    """
    Returns a dictionary of rotated images where keys are the rotation angles
    and the values are the rotated img
    img is a pygame image, rotation_angles is a list of rotation angles in
    degrees.
    If clockwise
        positive angles -->  clockwise rotations
        negative angles -->  anticlockwise rotations
    and vice versa if not clockwise
    """
    rotated_images = {}
    for rotation_angle in rotation_angles:
        if clockwise:
            rot_img = pg.transform.rotate(img, -rotation_angle)
        else:
            rot_img = pg.transform.rotate(img, rotation_angle)
        rotated_images[rotation_angle] = rot_img
    return rotated_images
