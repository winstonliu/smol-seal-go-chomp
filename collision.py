#!/bin/env python3

from observer import GameEventsManager, GameEvent

class CollisionEvent(GameEvent):
    COLLISION_KEYS = ["player_collision", "npc_collision"]

    def __init__(self, actor_a, actor_b, a_is_player):
        self.a = actor_a
        self.b = actor_b
        key = self.COLLISION_KEYS[0] if a_is_player else self.COLLISION_KEYS[1]
        super().__init__(key)

    def contains(self, actor):
        return actor == self.a or actor == self.b

    @classmethod
    def player_key(cls):
        return cls.COLLISION_KEYS[0]

    @classmethod
    def npc_key(cls):
        return cls.COLLISION_KEYS[1]

    @staticmethod
    def register_collision(actor_a, actor_b, a_is_player):
        new_collision = CollisionEvent(actor_a, actor_b, a_is_player)
        GameEventsManager.notify(new_collision.key, new_collision)


class CollisionMonitor:
    def __init__(self, actor_dict):
        # This is a pointer to the actor list and will get updated as the list
        # is updated
        # TODO create a dedicated class to hold actor objects
        self.actor_dict = actor_dict

    def check_player_collision(self):
        player = self.actor_dict["player"]
        for npc in self.actor_dict["npcs"]:
            if player.bounding_box().contains(npc.bounding_box()):
                print("Collision detected!")
                CollisionEvent.register_collision(player, npc, True)
