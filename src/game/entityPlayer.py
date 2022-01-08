import pygame
from functions import load_entity
from game.entity import Entity, EntityAlive, EntityGroups
from game.saveData import SaveData
from settings import Settings


image = load_entity("stay.png", "pirate")
image = pygame.transform.scale(image, (Settings.tileSize * 0.75, Settings.tileSize * 1.5))


class EntityPlayer(EntityAlive):
    def __init__(self, saveData: SaveData):
        super().__init__(None)
        self.saveData = saveData
        self.buttonPressed = [False, False, False, False]
        # нажаты ли кнопки движения в направлениях: вверх, вправо, вниз, влево (для корректного изменения направления движения)
        self.health = 5
        self.group = EntityGroups.playerSelf
        self.weapon: Entity = None
        self.message = ""
        self.image = image
        self.speed = 0.1
        self.width = 0.75
        self.height = 1
        self.imagePos = (0, -0.5)
        self.x = saveData.checkPointX + (1 - self.width) / 2
        self.y = saveData.checkPointY + (1 - self.height) / 2

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

        if (key == pygame.K_KP_4):
            self.screen.tryGoTo("left")
        if (key == pygame.K_KP_8):
            self.screen.tryGoTo("up")
        if (key == pygame.K_KP_6):
            self.screen.tryGoTo("right")
        if (key == pygame.K_KP_2):
            self.screen.tryGoTo("down")

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

    def update(self):
        return super().update()

    def preUpdate(self):
        self.message = ""
