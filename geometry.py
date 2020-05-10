#!/bin/env python3

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __add__(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return self + (-vec)

    def __iadd__(self, vec):
        self = self + vec
        return self

    def __isub__(self, vec):
        self += -vec
        return self

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


class Rectangle:
    def __init__(self, top_right_corner, size):
        self.top_right_corner = top_right_corner 
        self.size = size

class State:
    def __init__(self, position = Vector(0,0), velocity = Vector(0,0), acceleration = Vector(0,0)):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
