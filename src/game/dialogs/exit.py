import pygame
from typing import Callable
from functions import getPosMult, getRectMult, load_image, multPos as multPosFull
from game.gameDialog import GameDialog
from settings import Settings


multRect = getRectMult(Settings.width, Settings.height - Settings.overlay_height)
multPos = getPosMult(Settings.width, Settings.height - Settings.overlay_height)


class GameDialog_exit(GameDialog):
    multRectInner = getRectMult(*multPos((0.3, 0.5)))
    btnSize = multPosFull((1.6, 0.96), Settings.tileSize)
    yes_img = pygame.transform.scale(load_image("yes.png"), btnSize)
    no_img = pygame.transform.scale(load_image("no.png"), btnSize)
    yes_rect = multRectInner((0.1, 0.6, 0.36, 0.3))
    no_rect = multRectInner((0.55, 0.6, 0.36, 0.3))

    def __init__(self, onClose: Callable):
        super().__init__(onClose, *multPos((0.3, 0.5)))
        self.surface.blit(self.yes_img, self.yes_rect.topleft, (0, 0, self.yes_rect.width, self.yes_rect.height))
        self.surface.blit(self.no_img, self.no_rect.topleft)
        font = pygame.font.Font(Settings.path_font, int(Settings.tileSize * 0.58) + 1)
        text1 = font.render("Do you really", True, pygame.Color(81, 44, 40))
        text2 = font.render("want to quit?", True, pygame.Color(81, 44, 40))
        self.surface.blit(text1, multPos((0.025, 0.05)))
        self.surface.blit(text2, multPos((0.025, 0.15)))

    def onMouseUp(self, pos: tuple[int, int]):
        pos = super().onMouseUp(pos)
        if (self.yes_rect.collidepoint(pos)):
            self.closed = True
            self.onClose(True)
        if (self.no_rect.collidepoint(pos)):
            self.closed = True
            self.onClose(False)
