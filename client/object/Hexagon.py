from Object import Object
from math import sqrt

class Rectangle(Object):
    def __init__(self, x, y, radius, rotation=0, image=None):
        super().__init__(x, y, radius *2, radius * sqrt(3), rotation, image)

    def detect_click(self, mouse_x, mouse_y):
        correction = 0.95
        return (mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2 <= (self.radius ** 2) * correction
