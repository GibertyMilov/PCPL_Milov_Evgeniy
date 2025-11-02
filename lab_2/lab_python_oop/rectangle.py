from .figure import Figure
from .color import Color
import math


class Rectangle(Figure):
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color_property = Color(color)
        self._name = "Прямоугольник"

    def area(self):
        return self.width * self.height

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return "{}: ширина = {}, высота = {}, цвет = {}, площадь = {:.2f}".format(
            self.name, self.width, self.height, self.color_property.color, self.area()
        )