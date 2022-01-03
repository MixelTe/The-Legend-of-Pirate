import pygame
from game.entityPlayer import EntityPlayer
from settings import Settings


class Overlay:
    def __init__(self, player: EntityPlayer):
        self.surface = pygame.Surface((Settings.width, Settings.overlay_height))
        self.player = player

    def update() -> bool:
        #возвращает True, если игрок нажал "Выйти"
        pass

    def draw() -> pygame.Surface:
        # если player.message не пусто, то выводится это сообщение.
        pass

    def onClick(pos: tuple[int, int]):
        pass
