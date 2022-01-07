import pygame
from game.entityPlayer import EntityPlayer


class GamePopup:
    def close(self):
        pass

    def draw(self) -> pygame.Surface:
        pass

    def update(self):
        pass


class GamePopupDialog(GamePopup):
    def onMove(pos: tuple[int, int]):
        pass

    def onMouseUp(pos: tuple[int, int]):
        pass

    def onKeyUp(self, key):
        pass

    def onJoyHat(self, value):
        pass

    def onJoyAxis(self, axis, value):
        pass

    def onJoyButonUp(self, button):
        pass


class GamePopupTextbox(GamePopup):
    def __init__(self, player: EntityPlayer):
        self.pos = (0, 0)
        self.player = player
        self.opened = False

    def setText(text: str):
        pass
