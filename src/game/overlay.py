import pygame
from game.entityPlayer import EntityPlayer
from settings import Settings


class Overlay:
    def __init__(self, player: EntityPlayer):
        self.surface = pygame.Surface((Settings.width, Settings.overlay_height))
        self.player = player

    def update(self) -> bool:
        #возвращает True, если игрок нажал "Выйти"
        pass

    def draw(self) -> pygame.Surface:
        # если player.message не пусто, то выводится это сообщение.
        pass

    def onClick(self, pos: tuple[int, int]):
        pass
