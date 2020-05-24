#!/bin/env python3

import geometry
import events

class AddSpeedCommand:
    def __init__(self, unit, velocity):
        self.unit = unit
        self.velocity = velocity

    def execute(self):
        self.unit.add_velocity(self.velocity)


class Actor:
    MAX_VELOCITY = geometry.Vector(640.0, 360.0)

    def __init__(self, state = geometry.State(), is_player = False):
        self.state = state
        self.bounciness = 0
        self.is_player = is_player
        self.color = "white"
        self.bmin = self.bmax = geometry.Vector(0,0)

    # Define properties

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size

    @property
    def bounds(self):
        return (self.bmin, self.bmax)

    @bounds.setter
    def bounds(self, bounds_tuple):
        self.bmin = bounds_tuple[0]
        self.bmax = bounds_tuple[1]

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        self._sprite = sprite

    @property
    def bounciness(self):
        return self._bounciness

    @bounciness.setter
    def bounciness(self, bounciness):
        self._bounciness = bounciness

    @property
    def state(self):
        return self._state

    # TODO update state to output individual pos, vel, and accel
    
    @state.setter
    def state(self, state):
        """ State position is clamped to the actor bounds """
        self._state = state

    # Methods 

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
    def __init__(self):
        super().__init__(
                geometry.State(position = geometry.Vector(100,150)),
                is_player = True)
        self.size = geometry.Vector(50, 50)
        self.bounciness = 0.4
        self.state.acceleration = geometry.Vector(0, -0.005)
        self.delete = False

    def update(self):
        super().update()


class NpcFish(Actor):
    """ It's a fish! """
    def __init__(self, state, size):
        super().__init__(state)
        self.delete = False
        self.size = size

    def update(self):
        """ Destructive event checking """
        super().update()

        # Delete if we've hit the edge
        if self.state.position.x <= self.bmin.x:
            self.delete = True


class NpcShark(NpcFish):
    """ Chomp! """
    def __init__(self, state, size):
        super().__init__(state, size)
