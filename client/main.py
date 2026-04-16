import pygame
from eventHandler import eventHandler
from displayHandler import displayHandler
from object.Object import Object

def main():
    pygame.init()
    events = eventHandler()
    objects = [Object(50, 50, 50, 50, image_path="graphics/tmp.png")]
    display = displayHandler(800, 600, objects)
    clock = pygame.time.Clock()

    while(events.running):
        events.handle_events()
        display.run()
        pygame.display.flip()
        clock.tick(50)

if __name__ == "__main__":
    main()
    pygame.quit()