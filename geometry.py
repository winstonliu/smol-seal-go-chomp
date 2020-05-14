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
        self.x1 = top_right_corner.x
        self.y1 = top_right_corner.y
        self.x2 = top_right_corner.x + self.size.x
        self.y2 = top_right_corner.y + self.size.y

    def contains(self, rectangle):
        x_intersects = False
        y_intersects = False

        # Check if x intersects
        for x in [rectangle.x1, rectangle.x2]:
            if x >= self.x1 and x <= self.x2:
                x_intersects = True

        for y in [rectangle.y1, rectangle.y2]:
            if y >= self.y1 and y <= self.y2:
                y_intersects = True

        return x_intersects and y_intersects


class State:
    def __init__(self, position = Vector(0,0), velocity = Vector(0,0), acceleration = Vector(0,0)):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    def __str__(self):
        return "[" + "p:" + str(self.position) + "," + "v:" + str(self.velocity) + "," + "a:" + str(self.acceleration) + "]"
