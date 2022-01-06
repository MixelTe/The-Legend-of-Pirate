from typing import Literal, Union
import pygame
from functions import load_image
from game.entity import Entity, EntityAlive
from game.saveData import SaveData
from settings import Settings


image = load_image("crab.png")
image = image.subsurface(0, 0, 13, 11)
image = pygame.transform.scale(image, (Settings.tileSize * 0.8, Settings.tileSize * 0.677))


class EntityPlayer(EntityAlive):
    def __init__(self, saveData: SaveData):
        super().__init__(None)
        self.saveData = saveData
        self.buttonPressed = [False, False, False, False]
        # нажаты ли кнопки движения в направлениях: вверх, вправо, вниз, влево (для корректного изменения направления движения)
        self.weapon: Entity = None
        self.message = ""
        self.speed = 0.1
        self.x = saveData.checkPointX + (1 - self.width) / 2
        self.y = saveData.checkPointY + (1 - self.width) / 2

    def onKeyDown(self, key):
        if (key == pygame.K_w or key == pygame.K_UP):
            self.buttonPressed[0] = True
            self.speedY = -self.speed
        if (key == pygame.K_s or key == pygame.K_DOWN):
            self.buttonPressed[2] = True
            self.speedY = self.speed
        if (key == pygame.K_d or key == pygame.K_RIGHT):
            self.buttonPressed[1] = True
            self.speedX = self.speed
        if (key == pygame.K_a or key == pygame.K_LEFT):
            self.buttonPressed[3] = True
            self.speedX = -self.speed

    def onKeyUp(self, key):
        if (key == pygame.K_w or key == pygame.K_UP):
            self.buttonPressed[0] = False
            if (self.buttonPressed[2]):
                self.speedY = self.speed
            else:
                self.speedY = 0
        if (key == pygame.K_s or key == pygame.K_DOWN):
            self.buttonPressed[2] = False
            if (self.buttonPressed[0]):
                self.speedY = -self.speed
            else:
                self.speedY = 0
        if (key == pygame.K_d or key == pygame.K_RIGHT):
            self.buttonPressed[1] = False
            if (self.buttonPressed[3]):
                self.speedX = -self.speed
            else:
                self.speedX = 0
        if (key == pygame.K_a or key == pygame.K_LEFT):
            self.buttonPressed[3] = False
            if (self.buttonPressed[1]):
                self.speedX = self.speed
            else:
                self.speedX = 0

    def onJoyHat(self, value):
        self.buttonPressed = [False, False, False, False]
        if (value[1] > 0):
            self.speedY = -self.speed
        elif (value[1] < 0):
            self.speedY = self.speed
        else:
            self.speedY = 0
        if (value[0] > 0):
            self.speedX = self.speed
        elif (value[0] < 0):
            self.speedX = -self.speed
        else:
            self.speedX = 0

    def onJoyAxis(self, axis, value):
        if (axis == 0):
            self.speedX = self.speed * value
        if (axis == 1):
            self.speedY = self.speed * value

    def onJoyButonDown(self, button):
        pass

    def onJoyButonUp(self, button):
        pass
