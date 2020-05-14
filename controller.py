#!/bin/env python3

import config
from observer import GameEventsManager, GameEvent

""" Game controller """

class GameController:
    def __init__(self, set_timer_fcn):
        """ Use the timer set function to initialize the relevant events """
        # Create a new fish every two seconds
        set_timer_fcn(config.EVENT_MAPPING["CREATE_NEW_FISH"], int(2 * 1e6))

    def create_fish(self):
        pass
