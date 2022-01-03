import pygame
from settings import Settings


class ScreenAnimation:
    def __init__(self):
        self.surface = pygame.Surface((Settings.width, Settings.height - Settings.overlay_height))

    def update(self) -> bool:
        # возвращает флаг закончилась ли анимация
        pass

    def draw(self) -> pygame.Surface:
        # возвращает кадр анимации сдвига
        pass


class ScreenAnimationMove(ScreenAnimation):
    def __init__(self, imageOld: pygame.Surface, imageNew: pygame.Surface, direction: tuple[int, int]):
        # direction - значения 1, 0 или -1 сдвиг по x или y. На основе direction установка dx, dy и скорости
        self.imageOld = imageOld
        self.imageNew = imageNew
        self.dx = 0
        self.dy = 0
        self.speedX = 0
        self.speedY = 0


class ScreenAnimationBlur(ScreenAnimation):
    def __init__(self, image: pygame.Surface):
        self.image = image
        self.blurState = 0
