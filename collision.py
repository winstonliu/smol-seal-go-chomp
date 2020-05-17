#!/bin/env python3

import events

class CollisionMonitor:
    def __init__(self, actor_dict):
        # This is a pointer to the actor list and will get updated as the list
        # is updated
        # TODO create a dedicated class to hold actor objects
        self.actor_dict = actor_dict

    def check_player_collision(self):
        player = self.actor_dict["player"].actor
        for npc in self.actor_dict["npcs"]:
            if player.bounding_box().contains(npc.bounding_box()):
                events.CollisionEvent.register_collision(player, npc, True)
