#!/bin/env python3

import random

import actor
import config
import geometry

from observer import GameEventsManager, GameEvent

""" Game controller """

class NewActorEvent(GameEvent):
    def __init__(self, fish):
        super().__init__("actors_created")
        self.value = fish

class GameController:
    def __init__(self, set_timer_fcn):
        """ Use the timer set function to initialize the relevant events """
        # Create a new fish every two seconds
        set_timer_fcn(config.EVENT_MAPPING["CREATE_NEW_FISH"], int(2 * 1e3))

    def create_fish(self):
        fish_size = actor.NpcFish.SIZE

        fish_state = geometry.State()
        
        # Randomly generate a starting y
        fish_state.position.x = config.ScreenInfo.width - fish_size.x
        fish_state.position.y = random.randrange(config.ScreenInfo.height - fish_size.y)

        fish_state.velocity.x = -0.2

        new_fish = actor.NpcFish(fish_state)

        GameEventsManager.notify_with_event(NewActorEvent(new_fish))
