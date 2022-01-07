import pygame
from settings import Settings


class ScreenAnimation:
    def __init__(self):
        self.width = Settings.width
        self.height = Settings.height - Settings.overlay_height
        self.surface = pygame.Surface((self.width, self.height))

    def update(self) -> bool:
        return True

    def draw(self) -> pygame.Surface:
        return self.surface


class ScreenAnimationMove(ScreenAnimation):
    def __init__(self, imageOld: pygame.Surface, imageNew: pygame.Surface, direction: tuple[int, int]):
        super().__init__()
        # direction - значения 1, 0 или -1 сдвиг по x или y. На основе direction установка dx, dy и скорости
        self.imageOld = imageOld
        self.imageNew = imageNew
        self.dx = direction[0]
        self.dy = direction[1]
        self.counterX = 0
        self.counterY = 0
        time = 250 # ms
        self.speedX = direction[0] / time
        self.speedY = direction[1] / time

    def update(self) -> bool:
        self.counterX += self.speedX * (1000 / Settings.fps)
        self.counterY += self.speedY * (1000 / Settings.fps)
        return abs(self.counterX) >= 1 or abs(self.counterY) >= 1

    def draw(self) -> pygame.Surface:
        new_x = self.width * (self.dx - self.counterX)
        new_y = self.height * (self.dy - self.counterY)
        old_x = new_x - self.width * self.dx
        old_y = new_y - self.height * self.dy
        self.surface.blit(self.imageOld, (old_x, old_y))
        self.surface.blit(self.imageNew, (new_x, new_y))
        return self.surface


class ScreenAnimationBlur(ScreenAnimation):
    def __init__(self, imageOld: pygame.Surface, imageNew: pygame.Surface):
        super().__init__()
        self.surfaceRect = pygame.Surface((self.width, self.height))
        self.surfaceRect.fill(pygame.Color(0, 0, 0))
        self.imageOld = imageOld
        self.imageNew = imageNew
        self.blurState = 0
        self.counter = 0
        self.speed = 1 / 500
        self.pause = 200 # ms

    def update(self) -> bool:
        if (self.blurState == 0 or self.blurState == 2):
            self.counter += self.speed * (1000 / Settings.fps)
            if (self.counter >= 1):
                self.blurState += 1
                self.counter = 0
            return False
        if (self.blurState == 1):
            self.pause -= (1000 / Settings.fps)
            if (self.pause <= 0):
                self.blurState += 1
            return False
        return True

    def draw(self) -> pygame.Surface:
        blur = self.counter
        if (self.blurState == 0):
            self.surface.blit(self.imageOld, (0, 0))
        elif (self.blurState == 1):
            blur = 1
        elif (self.blurState == 2):
            blur = 1 - blur
            self.surface.blit(self.imageNew, (0, 0))
        self.surfaceRect.set_alpha(blur * 255)
        self.surface.blit(self.surfaceRect, (0, 0))
        return self.surface