#!/bin/env python3

import pygame

class ScreenInfo:
    size = width, height = 1280, 840


class MetaColor(type):
    """ 
    This lets me have more control over the colors used. 

    Don't actually use this class, it's a trick to let me use Color like a dictionary.
    
    """
    color_dictionary = {
            "black": (0,0,0),
            "blue": (135, 206, 235),
            "green": (144, 238, 144),
            "white": (255, 255, 255),
    }

    def __getitem__(cls, color):
        """ This function lets me treat the Color class like a read-only dictionary. """
        return pygame.Color(*cls.color_dictionary[color])

class Color(object, metaclass=MetaColor):
    pass


def rect_to_pygame(rectangle):
    return pygame.Rect(rectangle.top_right_corner.x, rectangle.top_right_corner.y , rectangle.size.x, rectangle.size.y)
