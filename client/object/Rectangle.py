from Object import Object
from math import abs

class Rectangle(Object):
    def __init__(self, x, y, width, height, rotation=0, image=None):
        super().__init__(x, y, width, height, rotation, image)

    def detect_click(self, mouse_x, mouse_y):
        return abs(mouse_x - self.x)*2 <= self.width and abs(mouse_y - self.y)*2 <= self.height
