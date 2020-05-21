#!/bin/env python3

import random

import actor
import config
import events
import game_assets
import geometry

""" Game controller """

class GameController:
    def __init__(self, fish_loader, shark_loader, set_timer_fcn):
        """ Use the timer set function to initialize the relevant events """
        # Create a new fish every two seconds
        set_timer_fcn(config.EVENT_MAPPING["CREATE_NEW_FISH"], int(2 * 1e3))
        # Need the 0.1 offset, when the timers overlap bad things happen
        set_timer_fcn(config.EVENT_MAPPING["CREATE_NEW_SHARK"], int(5.1 * 1e3))

        self.fish_loader = fish_loader
        self.shark_loader = shark_loader


    def create_npc(self, npc_type, npc_size):
        npc_state = geometry.State()

        npc_state.position.x = config.ScreenInfo.width - npc_size.x
        npc_state.position.y = random.randrange(config.ScreenInfo.height - npc_size.y)

        npc_state.velocity.x = -0.4
        new_npc = npc_type(npc_state)
        return new_npc


    def create_fish(self):
        fish_sprite = self.fish_loader.new_sprite()

        npc_size = geometry.Vector(*fish_sprite.rect.size)
        npc_fish = self.create_npc(actor.NpcFish, npc_size)

        fish_sprite.set_actor(npc_fish)
        events.GameEventsManager.notify_with_event(events.NewActorEvent(fish_sprite))


    def create_shark(self):
        shark_sprite = self.shark_loader.new_sprite()

        npc_size = geometry.Vector(*shark_sprite.rect.size)
        npc = self.create_npc(actor.NpcShark, npc_size)
        npc.state.velocity.x = -0.8

        shark_sprite.set_actor(npc)
        events.GameEventsManager.notify_with_event(events.NewActorEvent(shark_sprite))
