import pygame

class displayHandler:
    def __init__(self, width, height, objects):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("PyGame")
        self.objects = objects

    def clean_screen(self):
        self.screen.fill((0, 0, 0))

    def update_display(self):
        for object in self.objects:
            object.draw(self.screen)

    def run(self):
        self.clean_screen()
        self.update_display()
