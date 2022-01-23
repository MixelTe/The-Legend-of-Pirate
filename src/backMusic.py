import pygame


backMusic: str = None
curMusic: str = None


def setBackMusic(path, volume=1):
    global curMusic, backMusic
    curMusic = path
    backMusic = path
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)


def startMusicBreak(path, volume=1):
    global curMusic
    curMusic = path
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()


def getCurMusic():
    return curMusic


def onMusicEnd():
    global curMusic
    if (curMusic):
        curMusic = None
        pygame.mixer.music.load(backMusic)
        pygame.mixer.music.play(-1)
