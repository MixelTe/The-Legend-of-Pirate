import pygame
import os
from settings import Settings
from window import Window

# screen = pygame.display.set_mode((Settings.width, Settings.height), pygame.FULLSCREEN)
screen = pygame.display.set_mode((Settings.width, Settings.height))

from windowStart import WindowStart



class Main:
    def __init__(self):
        pygame.display.set_caption('The Legend of Pirate')
        self.window: Window = WindowStart()

    def start(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.window.on_event(event)

            result = self.window.calc()
            if (isinstance(result, Window)):
                self.window = result

            screen.fill((133, 133, 133))
            self.window.draw(screen)
            pygame.display.flip()

            clock.tick(60)

        pygame.quit()


if (__name__ == "__main__"):
    Main().start()
