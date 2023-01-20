import math


class ModuleFunction:
    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b

    def get_value(self, x):
        return abs(self.a * x + self.b)


class Polynom:
    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c

    def get_value(self, x):
        return self.a * math.pow(x, 2) + self.b * x + self.c
