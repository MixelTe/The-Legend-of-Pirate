import pygame
from settings import Settings
from window import Window

screen = pygame.display.set_mode((Settings.width, Settings.height), pygame.FULLSCREEN if Settings.fullscreen else 0)

from windowStart import WindowStart
from windowGame import WindowGame


class Main:
    def __init__(self):
        pygame.display.set_caption('The Legend of Pirate')
        # self.window: Window = WindowStart()
        self.window: Window = WindowGame(0) # Temp

    def start(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for i in range(pygame.joystick.get_count()):
                pygame.joystick.Joystick(i).init()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.window.on_event(event)

            result = self.window.update()
            if (isinstance(result, Window)):
                self.window = result

            screen.fill((133, 133, 133))
            self.window.draw(screen)
            pygame.display.flip()

            clock.tick(Settings.fps)

        pygame.quit()


pygame.joystick.init()
Main().start()
