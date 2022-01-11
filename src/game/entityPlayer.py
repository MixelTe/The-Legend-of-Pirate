import pygame
from game.animator import Animator, AnimatorData
from game.entity import Entity, EntityAlive, EntityGroups
from game.saveData import SaveData


animatorData = AnimatorData("pirate", [
    ("stay.png", 0, (12, 24), (0, -0.5, 0.75, 1.5)),
    ("goingS.png", 150, (12, 24), (0, -0.5, 0.75, 1.5)),
    ("goingW.png", 150, (12, 24), (0, -0.5, 0.75, 1.5)),
    ("goingA.png", 150, (12, 18), (-0.15, -0.5, 1, 1.5)),
    ("goingD.png", 150, (12, 18), (-0.05, -0.5, 1, 1.5)),
    ("attackS.png", 100, (12, 29), (0, -0.5, 0.75, 1.8)),
    ("attackW.png", 100, (12, 29), (0, -0.8, 0.75, 1.8)),
    ("attackA.png", 100, (21, 18), (-0.9, -0.5, 1.75, 1.5)),
    ("attackD.png", 100, (21, 18), (0, -0.5, 1.75, 1.5)),
    ("dig.png", 200, (21, 18), (0, -0.5, 1.75, 1.5)),
    ("swim.png", 150, (16, 24), (-0.1, -0.6, 1, 1.5)),
    ("swimW.png", 150, (16, 24), (-0.1, -0.6, 1, 1.5)),
    ("swimS.png", 150, (16, 24), (-0.1, -0.6, 1, 1.5)),
    ("swimA.png", 150, (16, 18), (-0.2, -0.5, 1.33, 1.5)),
    ("swimD.png", 150, (16, 18), (-0.2, -0.5, 1.33, 1.5)),
])


class EntityPlayer(EntityAlive):
    def __init__(self, saveData: SaveData):
        super().__init__(None)
        self.saveData = saveData
        self.buttonPressed = []
        # нажаты ли кнопки движения в направлениях: вверх, вправо, вниз, влево (для корректного изменения направления движения)
        self.health = 5
        self.group = EntityGroups.playerSelf
        self.weapon: Entity = None
        self.message = ""
        self.speed = 0.07
        self.width = 0.75
        self.height = 1
        self.imagePos = (0, -0.5)
        self.x = saveData.checkPointX + (1 - self.width) / 2
        self.y = saveData.checkPointY + (1 - self.height) / 2
        self.animator = Animator(animatorData, "stay")
        self.direction = None
        self.shovel = None
        self.digging = False

    def onKeyDown(self, key):
        if (key == pygame.K_w or key == pygame.K_UP):
            self.buttonPressed.append("up")
        if (key == pygame.K_s or key == pygame.K_DOWN):
            self.buttonPressed.append("down")
        if (key == pygame.K_d or key == pygame.K_RIGHT):
            self.buttonPressed.append("right")
        if (key == pygame.K_a or key == pygame.K_LEFT):
            self.buttonPressed.append("left")
        if (key == pygame.K_SPACE):
            self.attack()
        if (key == pygame.K_e):
            self.dig()

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
            while "up" in self.buttonPressed:
                self.buttonPressed.remove("up")
        if (key == pygame.K_s or key == pygame.K_DOWN):
            while "down" in self.buttonPressed:
                self.buttonPressed.remove("down")
        if (key == pygame.K_d or key == pygame.K_RIGHT):
            while "right" in self.buttonPressed:
                self.buttonPressed.remove("right")
        if (key == pygame.K_a or key == pygame.K_LEFT):
            while "left" in self.buttonPressed:
                self.buttonPressed.remove("left")

    def onJoyHat(self, value):
        if (value[1] > 0):
            while "down" in self.buttonPressed:
                self.buttonPressed.remove("down")
            self.buttonPressed.append("up")
        elif (value[1] < 0):
            while "up" in self.buttonPressed:
                self.buttonPressed.remove("up")
            self.buttonPressed.append("down")
        else:
            while "up" in self.buttonPressed:
                self.buttonPressed.remove("up")
            while "down" in self.buttonPressed:
                self.buttonPressed.remove("down")
        if (value[0] > 0):
            while "left" in self.buttonPressed:
                self.buttonPressed.remove("left")
            self.buttonPressed.append("right")
        elif (value[0] < 0):
            while "right" in self.buttonPressed:
                self.buttonPressed.remove("right")
            self.buttonPressed.append("left")
        else:
            while "right" in self.buttonPressed:
                self.buttonPressed.remove("right")
            while "left" in self.buttonPressed:
                self.buttonPressed.remove("left")

    def onJoyAxis(self, axis, value):
        if (axis == 0):
            if (value > 0.5):
                while "left" in self.buttonPressed:
                    self.buttonPressed.remove("left")
                self.buttonPressed.append("right")
            elif (value < -0.5):
                while "right" in self.buttonPressed:
                    self.buttonPressed.remove("right")
                self.buttonPressed.append("left")
            else:
                while "right" in self.buttonPressed:
                    self.buttonPressed.remove("right")
                while "left" in self.buttonPressed:
                    self.buttonPressed.remove("left")
        if (axis == 1):
            print(value)
            if (value > 0.5):
                while "up" in self.buttonPressed:
                    self.buttonPressed.remove("up")
                self.buttonPressed.append("down")
            elif (value < -0.5):
                while "down" in self.buttonPressed:
                    self.buttonPressed.remove("down")
                self.buttonPressed.append("up")
            else:
                while "up" in self.buttonPressed:
                    self.buttonPressed.remove("up")
                while "down" in self.buttonPressed:
                    self.buttonPressed.remove("down")

    def onJoyButonDown(self, button):
        pass

    def onJoyButonUp(self, button):
        pass

    def setSpeed(self):
        self.speedX = 0
        self.speedY = 0
        if (self.shovel is not None or self.digging):
            return
        if (len(self.buttonPressed) > 0):
            if (self.buttonPressed[-1] == "up"):
                self.speedY = -self.speed
                self.direction = "W"
            if (self.buttonPressed[-1] == "down"):
                self.speedY = self.speed
                self.direction = "S"
            if (self.buttonPressed[-1] == "right"):
                self.speedX = self.speed
                self.direction = "D"
            if (self.buttonPressed[-1] == "left"):
                self.speedX = -self.speed
                self.direction = "A"
        else:
            self.direction = None

    def attack(self):
        if (self.shovel is not None or self.digging):
            return
        self.shovel = Entity.createById("shovel", self.screen)
        self.screen.addEntity(self.shovel)
        self.shovel.startX = self.x
        self.shovel.startY = self.y
        self.shovel.direction = self.direction
        self.shovel.nextStage()

    def dig(self):
        if (self.shovel is not None or self.digging):
            return
        tile = self.get_tile(1, pos=(0.5, 0.7))
        if (tile.digable):
            self.digging = True

    def afterDig(self):
        coin = Entity.createById("coin", self.screen)
        self.screen.addEntity(coin)
        coin.x = self.x + 1.25
        coin.y = self.y + 0.5

    def update(self):
        self.setSpeed()
        super().update()

        if (self.digging):
            self.animator.setAnimation("dig")
            if (self.animator.lastState[1]):
                self.digging = False
                self.afterDig()
        elif (self.shovel is not None):
            if (self.direction):
                self.animator.setAnimation("attack" + self.direction)
            else:
                self.animator.setAnimation("attackS")
            if (self.animator.lastState[1]):
                self.shovel.remove()
                self.shovel = None
            elif (self.animator.lastState[0]):
                self.shovel.nextStage()
        else:
            tile = self.get_tile(pos=(0.5, 0.7))
            if (tile and "water" in tile.tags):
                if (self.direction):
                    self.animator.setAnimation("swim" + self.direction)
                else:
                    self.animator.setAnimation("swim")
            else:
                if (self.direction):
                    self.animator.setAnimation("going" + self.direction)
                else:
                    self.animator.setAnimation("stay")

    def preUpdate(self):
        self.message = ""
