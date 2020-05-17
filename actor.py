#!/bin/env python3

import geometry
from observer import GameEventsManager, GameEvent
from collision import CollisionEvent

class AddSpeedCommand:
    def __init__(self, unit, velocity):
        self.unit = unit
        self.velocity = velocity

    def execute(self):
        self.unit.add_velocity(self.velocity)


class Actor:
    MAX_VELOCITY = geometry.Vector(640.0, 360.0)

    def __init__(self, state = geometry.State(), size = geometry.Vector(0,0), bounciness = 0, is_player = False):
        self.state = state
        self.bounciness = bounciness 
        self.size = size
        self.is_player = is_player
        self.color = "white"

    def set_bounds(self, bounds_min, bounds_max):
        self.bmin = bounds_min
        self.bmax = bounds_max

    def update(self):
        self.state.velocity += self.state.acceleration
        new_position = self.state.position + self.state.velocity

        # Correct bounds for actor size
        bounds_max = self.bmax - self.size

        # Bounciness behaviour
        if new_position.x > bounds_max.x or new_position.x < self.bmin.x:
            self.state.velocity.x = -self.state.velocity.x * self.bounciness
        if new_position.y > bounds_max.y or new_position.y < self.bmin.y:
            self.state.velocity.y = -self.state.velocity.y * self.bounciness

        # Bound the position
        new_position.x = max(min(new_position.x, bounds_max.x), self.bmin.x)
        new_position.y = max(min(new_position.y, bounds_max.y), self.bmin.y)

        self.state.position = new_position

    def add_velocity(self, velocity):
        new_velocity = self.state.velocity + velocity

        self.state.velocity.x = min(new_velocity.x, self.MAX_VELOCITY.x)
        self.state.velocity.y = min(new_velocity.y, self.MAX_VELOCITY.y)

    def bounding_box(self):
        return geometry.Rectangle(self.state.position, self.size)


    def draw(self):
        return geometry.Rectangle(self.state.position, self.size)


class PlayerSeal(Actor):
    """ This class takes care of all player related stuff. """
    SIZE = geometry.Vector(50, 50)
    def __init__(self):
        super().__init__(
                geometry.State(position = geometry.Vector(100,100)),
                self.SIZE, 
                0.2,
                is_player = True)
        self.state.acceleration = geometry.Vector(0, -0.005)

    def update(self):
        super().update()


class NpcFish(Actor):
    """ It's a fish! """
    SIZE = geometry.Vector(10, 10)
    def __init__(self, state):
        super().__init__(state, self.SIZE)
        self.delete = False
        self.color = "red"

    def update(self):
        """ Destructive event checking """
        super().update()

        # Delete if we've hit the player
        result = GameEventsManager.consume_event_for_value(CollisionEvent.player_key(), self)
        # Delete if we've hit the edge, including a fudge factor
        if len(result) > 0 or self.state.position.x <= self.bmin.x + 1:
            self.delete = True


class AteBySharkEvent(GameEvent):
    def __init__(self):
        super().__init__("got_eaten")


class NpcShark(Actor):
    """ Chomp! """
    SIZE = geometry.Vector(75, 25)
    def __init__(self, state):
        super().__init__(state, self.SIZE)
        self.delete = False
        self.color = "purple"

    def update(self):
        """ Destructive event checking """
        super().update()

        # Delete if we've hit the edge, including a fudge factor
        if self.state.position.x <= self.bmin.x + 1:
            self.delete = True

        # Trigger an end game event if we've hit the player
        result = GameEventsManager.consume_event_for_value(CollisionEvent.player_key(), self)
        if len(result) > 0:
            GameEventsManager.notify_with_event(AteBySharkEvent())
