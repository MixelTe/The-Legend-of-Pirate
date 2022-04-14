from random import random
import pygame
from functions import calcPlayerCoinsAfterDeath, load_image, scaleImg
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
        time = 250  # ms
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
        self.pause = 200  # ms

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


class ScreenAnimationDeath(ScreenAnimation):
    coin = scaleImg(load_image("coin.png"), 0.33, 0.4)

    def __init__(self, image: pygame.Surface, player):
        super().__init__()
        self.surfaceRect = pygame.Surface((self.width, self.height))
        self.surfaceRect.fill(pygame.Color(0, 0, 0))
        self.image = image
        self.player = player
        self.counter = self.width
        self.counter2 = 0
        self.playerCoins = calcPlayerCoinsAfterDeath(self.player.saveData.tags, self.player.saveData.coins)
        self.counter3 = 0
        self.coins = []  # {"x": 0, "y": 0, "speedX": 0, "speedY": 0}

    def update(self) -> bool:
        self.counter = max(self.counter - 20, 0)
        self.counter2 = min(self.counter2 + 1, 40)
        self.counter3 += 1
        if (self.counter3 >= 10):
            self.counter3 = 0
            if (self.player.saveData.coins > self.playerCoins):
                self.player.saveData.coins -= 1
                self.coins.append({"x": self.player.x, "y": self.player.y, "speedX": (random() - 0.5) * 0.2, "speedY": 0})
        for coin in self.coins:
            coin["x"] += coin["speedX"]
            coin["y"] += coin["speedY"]
            coin["speedY"] += 0.005
        self.player.update()
        return self.player.state == "dead"

    def draw(self) -> pygame.Surface:
        self.surface.blit(self.image, (0, 0))
        self.surfaceRect.fill(pygame.Color(40, 40, 40))
        center = ((self.player.x + self.player.width / 2) * Settings.tileSize,
                  (self.player.y + self.player.height / 2) * Settings.tileSize)
        pygame.draw.circle(self.surfaceRect, pygame.Color(255, 255, 255), center, self.counter)
        self.surface.blit(self.surfaceRect, (0, 0), special_flags=pygame.BLEND_MULT)
        pygame.draw.circle(self.surface, pygame.Color(200, 200, 255), center, self.counter2)
        for coin in self.coins:
            self.surface.blit(self.coin, (coin["x"] * Settings.tileSize, coin["y"] * Settings.tileSize))
        self.player.draw(self.surface)
        return self.surface
