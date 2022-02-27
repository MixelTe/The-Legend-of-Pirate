import pygame
from backMusic import onMusicEnd, setBackMusic
from fpsGraph import FpsGraph
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
        # self.window: Window = WindowStart()
        self.window: Window = WindowGame(0)
        self.fpsGraph = FpsGraph()

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
                if event.type == musicEndEvent:
                    onMusicEnd()
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_F3):
                        self.fpsGraph.enabled = not self.fpsGraph.enabled
                self.window.on_event(event)

            result = self.window.update()
            if (isinstance(result, Window)):
                self.window = result

            screen.fill((133, 133, 133))
            self.window.draw(screen)
            if (self.fpsGraph.enabled):
                self.fpsGraph.draw(screen)
            pygame.display.flip()

            time = clock.tick(Settings.fps)
            if (self.fpsGraph.enabled):
                self.fpsGraph.add(time)


pygame.joystick.init()
pygame.display.set_caption('The Legend of Pirate')
musicEndEvent = pygame.event.custom_type() + 1
pygame.mixer.music.set_endevent(musicEndEvent)
setBackMusic(joinPath(Settings.folder_data, Settings.folder_sounds, "back", "background.mp3"))
Main().start()
pygame.mixer.quit()
pygame.quit()
