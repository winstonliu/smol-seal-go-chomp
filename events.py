#!/bin/env python3
""" This file implements an observer pattern. """

class GameEvent:
    """ Parent class for game events """
    def __init__(self, key):
        self.key = key
        self.value = None

    def contains(self, value):
        return value == self.value


class GameEventsManager:
    """ Singleton class managing an events object. """
    # Static events dictionary
    events = dict()

    @classmethod
    def notify(cls, key, value):
        if not key in cls.events:
            cls.events[key] = [value]
        else:
            cls.events[key].append(value)

    @classmethod
    def notify_with_event(cls, event):
        cls.notify(event.key, event)

    @classmethod
    def consume(cls, key):
        if key in cls.events:
            ret_val = cls.events[key]
            del cls.events[key]
            return ret_val
        return None

    @classmethod
    def peek(cls, key):
        if key in cls.events:
            return cls.events[key]
        return None

    @classmethod
    def consume_event_for_value(cls, key, value):
        result_list = cls.peek(key)
        if result_list:
            output_list = [x for x in result_list if x.contains(value)]
            # Remove output list elements from base list
            for x in output_list:
                result_list.remove(x)
            return output_list
        return list()


class NewActorEvent(GameEvent):
    def __init__(self, npc):
        super().__init__("actors_created")
        self.value = npc


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


class AteBySharkEvent(GameEvent):
    def __init__(self):
        super().__init__("got_eaten")

class AteFishEvent(GameEvent):
    def __init__(self):
        super().__init__("ate_fish")

