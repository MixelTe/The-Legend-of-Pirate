import pygame
from settings import Settings

screen = pygame.display.set_mode((Settings.width, Settings.height), pygame.FULLSCREEN)

from window import Window



class Main:
    def __init__(self):
        pygame.display.set_caption('The Legend of Pirate')
        self.window = Window()

    def start(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.window.draw(screen)

            clock.tick(60)

        pygame.quit()


if (__name__ == "__main__"):
    Main().start()
