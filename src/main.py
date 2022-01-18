import pygame
from functions import joinPath
from settings import Settings

pygame.init()
screen = pygame.display.set_mode((Settings.width, Settings.height), pygame.FULLSCREEN if Settings.fullscreen else 0)
pygame.mixer.init()

from window import Window
from windowStart import WindowStart
from windowGame import WindowGame


class Main:
    def __init__(self):
        self.window: Window = WindowStart()
        # self.window: Window = WindowGame(0)  # Temp

    def start(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            joysticks = []
            for i in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                joysticks.append(joystick)

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


pygame.joystick.init()
pygame.display.set_caption('The Legend of Pirate')
pygame.mixer.music.load(joinPath(Settings.folder_data, Settings.folder_sounds, "background2.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
Main().start()
pygame.mixer.quit()
pygame.quit()
