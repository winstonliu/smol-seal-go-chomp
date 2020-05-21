#!/bin/env python3

import pygame

EVENT_MAPPING = {
        "CREATE_NEW_FISH" : pygame.USEREVENT,
        "CREATE_NEW_SHARK" : pygame.USEREVENT + 1,
}

class ScreenInfo:
    size = width, height = 1280, 840
    font = None

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
            "red": (252, 3, 115),
            "purple": (191, 66, 245),
    }

    def __getitem__(cls, color):
        """ This function lets me treat the Color class like a read-only dictionary. """
        return pygame.Color(*cls.color_dictionary[color])

class Color(object, metaclass=MetaColor):
    pass
