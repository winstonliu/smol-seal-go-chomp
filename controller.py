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
        # Need the 0.1 offset, when the timers overlap bad things happen
        set_timer_fcn(config.EVENT_MAPPING["CREATE_NEW_SHARK"], int(5.1 * 1e3))


    def create_npc(self, npc_type):
        npc_size = npc_type.SIZE
        npc_state = geometry.State()

        npc_state.position.x = config.ScreenInfo.width - npc_size.x - 1
        npc_state.position.y = random.randrange(config.ScreenInfo.height - npc_size.y)

        npc_state.velocity.x = -0.2
        new_npc = npc_type(npc_state)
        GameEventsManager.notify_with_event(NewActorEvent(new_npc))
