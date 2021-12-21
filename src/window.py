import pygame
from temp_pirate import Pirate
from start import WindowStart

now = 'start'


class Window():
    def __init__(self):
        self.pirate = Pirate()
        self.start = WindowStart()

    def draw(self, screen):
        if now == 'start':

            screen.fill((0, 0, 0))
            self.start.draw(screen)

            pygame.display.flip()

        if now == 'pirate':
            self.pirate.update()

            screen.fill((0, 0, 0))
            self.pirate.draw(screen)

            pygame.display.flip()


