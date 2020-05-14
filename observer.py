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
            cls.events[key] = list(value)
        else:
            cls.events[key].append(value)

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
