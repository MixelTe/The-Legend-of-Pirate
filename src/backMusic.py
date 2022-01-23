import pygame


backMusic: str = None
curMusic: str = None


def setBackMusic(path):
    global curMusic, backMusic
    curMusic = path
    backMusic = path
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1)


def startMusicBreak(path):
    global curMusic
    curMusic = path
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()


def getCurMusic():
    return curMusic


def onMusicEnd():
    global curMusic
    if (curMusic):
        curMusic = None
        pygame.mixer.music.load(backMusic)
        pygame.mixer.music.play(-1)
