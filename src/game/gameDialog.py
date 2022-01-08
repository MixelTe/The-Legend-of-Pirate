from typing import Callable
import pygame
from settings import Settings


class GameDialog:
    def __init__(self, onClose=lambda: None, w=10, h=10):
        self.onClose = onClose
        self.rect = pygame.Rect(0, 0, w, h)
        self.surface = pygame.Surface(self.rect.size)
        self.closed = False

    def draw(self) -> pygame.Surface:
        return self.surface

    def update(self) -> bool:
        return self.closed

    def onMove(self, pos: tuple[int, int]):
        pass

    def onMouseUp(self, pos: tuple[int, int]):
        if (not self.rect.collidepoint(pos)):
            self.closed = True

    def onKeyUp(self, key):
        pass

    def onJoyHat(self, value):
        pass

    def onJoyAxis(self, axis, value):
        pass

    def onJoyButonUp(self, button):
        pass


class GameDialog_exit(GameDialog):
    def __init__(self, onClose: Callable):
        super().__init__(onClose, Settings.width * 0.3, (Settings.height - Settings.overlay_height) * 0.5)
        self.rect.x = (Settings.width - self.rect.width) / 2
        self.rect.y = (Settings.height - Settings.overlay_height - self.rect.height) / 2
