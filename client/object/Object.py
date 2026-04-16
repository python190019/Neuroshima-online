import pygame


class Object:
    def __init__(self, x, y, width, height, rotation = 0, image_path = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.image = None
        if image_path is not None:
            self.set_image(image_path)

    def set_rotation(self, rotation):
        self.rotation = rotation

    def set_image(self, image_path):
        try:
            loaded = pygame.image.load(image_path)
            self.image = loaded.convert_alpha()
        except pygame.error as error:
            print(f"Nie mozna zaladowac obrazu '{image_path}': {error}")
            self.image = None

    def draw(self, surface=None):
        if self.image is None:
            return

        if surface is None:
            return

        image = pygame.transform.scale(self.image, (self.width, self.height))
        rotated_image = pygame.transform.rotate(image, self.rotation)

        center = (self.x + self.width / 2, self.y + self.height / 2)
        draw_rect = rotated_image.get_rect(center=center)
        surface.blit(rotated_image, draw_rect.topleft)

    def move(self, x, y):
        self.x = x
        self.y = y

    def detect_click(self, mouse_x, mouse_y):
        # do nadpisania przez klasy potomne
        return False
