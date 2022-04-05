import pygame


backMusic: str = None
backMusicVolume = 1
curMusic: str = None
battleMusic = None  # [0, mainPath, endPath]


def _startMusic(path, volume=1, count=0):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(count)


def setBackMusic(path, volume=1):
    global curMusic, backMusic, backMusicVolume
    curMusic = path
    backMusic = path
    backMusicVolume = volume
    _startMusic(path, volume, -1)


def startMusicBreak(path, volume=1):
    global curMusic
    curMusic = path
    _startMusic(path, volume)


def getCurMusic():
    return curMusic


def onMusicEnd():
    global curMusic
    if (battleMusic):
        if (battleMusic[0] == 0):
            _startMusic(battleMusic[2], battleMusic[1], -1)
            battleMusic[0] = 1
        if (battleMusic[0] == 2):
            _startMusic(backMusic, backMusicVolume, -1)
            battleMusic[0] = 1
    elif (curMusic):
        curMusic = None
        _startMusic(backMusic, backMusicVolume, -1)


def startBattleMusic(startPath, mainPath, endPath, volume=1):
    global battleMusic, curMusic
    battleMusic = [0, volume, mainPath, endPath]
    _startMusic(startPath, volume)


def endBattleMusic():
    battleMusic[0] = 2
    _startMusic(battleMusic[3], battleMusic[1])
