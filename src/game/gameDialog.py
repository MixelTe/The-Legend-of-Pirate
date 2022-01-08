import pygame


class GameDialog:
    def __init__(self):
        self.pos = (0, 0)

    def draw(self) -> pygame.Surface:
        pass

    def update(self):
        pass

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
