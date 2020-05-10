#!/bin/env python3

import geometry

class AddSpeedCommand:
    def __init__(self, unit, velocity):
        self.unit = unit
        self.velocity = velocity

    def execute(self):
        self.unit.add_velocity(self.velocity)


class Actor:
    MAX_VELOCITY = geometry.Vector(640.0, 360.0)

    def __init__(self):
        self.state = geometry.State()
        self.bounciness = 0
        self.size = geometry.Vector(0,0)

    def update(self, bounds_min, bounds_max):
        self.state.velocity += self.state.acceleration
        new_position = self.state.position + self.state.velocity

        # Correct bounds for actor size
        bounds_max -= self.size

        # Bounciness behaviour
        if new_position.x > bounds_max.x or new_position.x < bounds_min.x:
            self.state.velocity.x = -self.state.velocity.x * self.bounciness
        if new_position.y > bounds_max.y or new_position.y < bounds_min.y:
            self.state.velocity.y = -self.state.velocity.y * self.bounciness

        # Bound the position
        new_position.x = max(min(new_position.x, bounds_max.x), bounds_min.x)
        new_position.y = max(min(new_position.y, bounds_max.y), bounds_min.y)

        self.state.position = new_position

    def add_velocity(self, velocity):
        new_velocity = self.state.velocity + velocity

        self.state.velocity.x = min(new_velocity.x, self.MAX_VELOCITY.x)
        self.state.velocity.y = min(new_velocity.y, self.MAX_VELOCITY.y)

class PlayerSeal(Actor):
    """ This class takes care of all player related stuff. """

    def __init__(self):
        super().__init__()
        self.state.position = geometry.Vector(100,100)
        self.size = geometry.Vector(50,50)
        self.bounciness = 0.2
        self.state.acceleration = geometry.Vector(0, -0.005)


    def draw(self):
        return geometry.Rectangle(self.state.position, self.size)

    def update(self, bounds_min, bounds_max):
        super().update(bounds_min, bounds_max)
