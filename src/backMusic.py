from random import randint
import pygame

from functions import joinPath
from settings import Settings


backMusic: str = None
curMusic: str = None
loop = -1
loopPath = joinPath(Settings.folder_data, Settings.folder_sounds, "back", "loop")


def setBackMusic(path=None, volume=1):
    global curMusic, backMusic, loop
    curMusic = path
    backMusic = path
    if (backMusic):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
    else:
        loop = -1
        playLoop()


def startMusicBreak(path, volume=1):
    global curMusic
    curMusic = path
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()


def getCurMusic():
    return curMusic


def playLoop():
    global loop
    if (loop == -1):
        loop = 0
        pygame.mixer.music.load(joinPath(loopPath, f"intro.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()
    elif (loop == -2):
        loop = -3
        pygame.mixer.music.load(joinPath(loopPath, f"outro.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()
    elif (loop >= 0):
        # loop = (loop + 1) % 13
        loop = randint(0, 12)
        pygame.mixer.music.load(joinPath(loopPath, f"{loop}.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()


def onMusicEnd():
    global curMusic, loop
    if (curMusic):
        curMusic = None
        if (backMusic):
            pygame.mixer.music.load(backMusic)
            pygame.mixer.music.play(-1)
        else:
            loop = -1
            playLoop()
    elif (backMusic is None):
        playLoop()
