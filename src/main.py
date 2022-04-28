import pygame
from backMusic import onMusicEnd, setBackMusic
from fpsGraph import FpsGraph
from functions import joinPath, load_image, saveErrorFile
from settings import Settings, setSizes
import traceback
from sys import exit

pygame.init()
desktop_sizes = pygame.display.get_desktop_sizes()
if (len(desktop_sizes) == 0):
    exit()
desktop_size = desktop_sizes[0]
setSizes(desktop_size)
if (Settings.windowed):
    desktop_size = (Settings.width, Settings.height)
screen = pygame.display.set_mode(desktop_size, pygame.FULLSCREEN if Settings.fullscreen else 0)
img_loading = pygame.transform.scale(load_image("loading.png"), (Settings.width, Settings.height))
screen.blit(img_loading, ((desktop_size[0] - Settings.width) // 2, (desktop_size[1] - Settings.height) // 2))
pygame.display.flip()
pygame.mixer.init()

from window import Window
from windowStart import WindowStart
from windowGame import WindowGame
from windowAnimationTest import WindowAnimationTest
from windowEndGame import WindowEndGame
from game.saveData import SaveData


class Main:
    def __init__(self):
        # self.window: Window = WindowStart()
        # self.window: Window = WindowGame(0)
        # self.window: Window = WindowAnimationTest()
        self.window: Window = WindowEndGame(SaveData(1).load())
        self.surface = pygame.Surface((Settings.width, Settings.height))
        self.surfacePos = ((desktop_size[0] - Settings.width) // 2, (desktop_size[1] - Settings.height) // 2)
        self.fpsGraph = FpsGraph()
        font = pygame.font.Font(Settings.path_font, int(Settings.tileSize * 0.5))
        self.renderedText_AIDisabled = font.render("AI Disabled", True, "red")
        self.renderedText_DeathMouse = font.render("Death Mouse", True, "red")

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
                if (event.type == pygame.MOUSEMOTION or
                    event.type == pygame.MOUSEBUTTONDOWN or
                        event.type == pygame.MOUSEBUTTONUP):
                    event.pos = (event.pos[0] - self.surfacePos[0], event.pos[1] - self.surfacePos[1])
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_F3):
                        self.fpsGraph.enabled = not self.fpsGraph.enabled
                    if (Settings.DEVMode):
                        if (event.key == pygame.K_F1):
                            Settings.drawHitboxes = not Settings.drawHitboxes
                        if (event.key == pygame.K_F4):
                            Settings.disableAI = not Settings.disableAI
                        if (event.key == pygame.K_F5):
                            Settings.ghostmode = not Settings.ghostmode
                        if (event.key == pygame.K_F6):
                            Settings.drawGrid = not Settings.drawGrid
                        if (event.key == pygame.K_F7):
                            Settings.deathMouse = not Settings.deathMouse
                self.window.on_event(event)

            result = self.window.update()
            if (isinstance(result, Window)):
                self.window = result

            screen.fill((0, 0, 0))
            self.surface.fill((0, 0, 0))
            self.window.draw(self.surface)
            screen.blit(self.surface, self.surfacePos)
            if (self.fpsGraph.enabled):
                self.fpsGraph.draw(screen)
            if (Settings.disableAI):
                screen.blit(self.renderedText_AIDisabled, (Settings.tileSize * 0.2, Settings.height - Settings.tileSize * 0.6))
            if (Settings.deathMouse):
                screen.blit(self.renderedText_DeathMouse, (Settings.tileSize * 3.2, Settings.height - Settings.tileSize * 0.6))
            pygame.display.flip()

            time = clock.tick(Settings.fps)
            if (self.fpsGraph.enabled):
                self.fpsGraph.add(time)


def errorMessage():
    screen.fill((0, 0, 0))
    screen.blit(img_error, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
            if event.type == pygame.JOYBUTTONDOWN:
                return


pygame.joystick.init()
pygame.display.set_caption('The Legend of Pirate')
icon = pygame.transform.scale(load_image("icon.ico"), (32, 32))
img_error = pygame.transform.scale(load_image("error.png"), (Settings.width, Settings.height))
pygame.display.set_icon(icon)
musicEndEvent = pygame.event.custom_type() + 1
pygame.mixer.music.set_endevent(musicEndEvent)
setBackMusic(joinPath(Settings.folder_data, Settings.folder_sounds, "back", "SandWorld.mp3"))
try:
    Main().start()
except Exception as x:
    saveErrorFile(x, traceback.format_exc())
    errorMessage()
pygame.mixer.quit()
pygame.quit()
