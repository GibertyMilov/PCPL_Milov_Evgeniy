from .figure import Figure
from .color import Color
import math


class Circle(Figure):
    def __init__(self, radius, color):
        self.radius = radius
        self.color_property = Color(color)
        self._name = "Круг"

    def area(self):
        return math.pi * self.radius ** 2

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return "{}: радиус = {}, цвет = {}, площадь = {:.2f}".format(
            self.name, self.radius, self.color_property.color, self.area()
        )