import math
from typing import Any, Callable, Literal, Union
import pygame
from functions import drawPie
from game.animator import Animator, AnimatorData
from game.entity import EntityAlive, EntityGroups
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("aborigine", [
    ("stay.png", 0, (15, 16), (-0.241, -0.6, 1.2, 1.3)),
    ("moveD.png", 150, (15, 16), (-0.241, -0.6, 1.2, 1.3)),
    ("moveA.png", 150, (15, 16), (-0.591, -0.6, 1.2, 1.3)),
    ("attackD.png", 250, (15, 16), (-0.241, -0.6, 1.2, 1.3)),
    ("attackA.png", 250, (15, 16), (-0.591, -0.6, 1.2, 1.3)),
])


class EntityAborigine(EntityAlive):
    def __init__(self, screen, data: dict = None):
        self.type = "stay"  # stay, patrol
        self.rotate = False
        self.path = []
        self.sightDir = 0
        self.sightDirCur = 0
        super().__init__(screen, data)
        self.startPos = (int(self.x), int(self.y))
        self.animator = Animator(animatorData, "stay")
        self.group = EntityGroups.enemy
        self.speed = 0.05
        self.strength = 0
        self.healthMax = 2
        self.health = 2
        self.width = 0.32
        self.height = 0.7
        self.state = "stay"
        self.nextTile = 1
        self.lookR = 4
        self.forward = True
        self.seePlayer = 0
        self.sightZoneVisible = True
        self.rotationSpeed = 0.01
        self.stayTime = 0

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        dataSetter("type", self.type)
        dataSetter("rotate", self.rotate)
        dataSetter("path", self.path)
        if (self.path and len(self.path) <= 1):
            self.type = "stay"
        if ("direction" in data):
            self.setSightDir(data["direction"])

    def canGoOn(self, tile: Tile) -> bool:
        return "water" not in tile.tags and super().canGoOn(tile)

    def onDeath(self):
        coin = EntityAlive.createById("coin", self.screen)
        self.screen.addEntity(coin)
        coin.x = self.x + self.width / 2
        coin.y = self.y + self.height / 2

    def draw(self, surface: pygame.Surface, opaque=1):
        super().draw(surface, opaque)
        if (not self.sightZoneVisible):
            return
        p1 = ((self.x + self.width / 2) * Settings.tileSize, (self.y + self.height / 2) * Settings.tileSize)
        color = pygame.Color(255, 165, 0, 50)
        drawPie(surface, color, p1, self.lookR * Settings.tileSize,
                self.sightDirCur - math.pi / 4, self.sightDirCur + math.pi / 4, alpha=True)
        if (self.seePlayer):
            color = pygame.Color(255, 60, 0, 50)
            drawPie(surface, color, p1, self.lookR * self.seePlayer * Settings.tileSize,
                    self.sightDirCur - math.pi / 4, self.sightDirCur + math.pi / 4, alpha=True)
        # drawPie(surface, "gray", p1, self.lookR * Settings.tileSize,
        #         self.lookDirCur - math.pi / 4, self.lookDirCur + math.pi / 4, 1)

    def update(self):
        super().update()
        if (not self.alive or Settings.disableAI):
            return

        if (self.state == "stay"):
            self.stayTime -= max(1000 / Settings.fps, 0)
            if (self.type == "patrol"):
                if (self.stayTime <= 0):
                    self.state = "patrol"
                    nextX, nextY = self.path[self.nextTile]
                    if (abs(int(self.x) - nextX) == 0):
                        self.setSightDir("down" if int(self.x) < nextY else "up")
                    else:
                        self.setSightDir("right" if int(self.x) < nextX else "left")
                    self.animator.setAnimation("moveA" if int(self.x) < nextX else "moveD")
            self.sightDirCur += self.rotationSpeed
            if (abs(self.sightDirCur - self.sightDir) > 20 / 180 * math.pi):
                self.rotationSpeed *= -1
            if (self.checkPlayer()):
                self.state = "attack"
        elif (self.state == "patrol"):
            nextX, nextY = self.path[self.nextTile]
            dx = (nextX + 0.5) - (self.x + self.width / 2)
            dy = (nextY + 0.5) - (self.y + self.height / 2)
            if (abs(dx) <= 0.01 and abs(dy) <= 0.01):
                pathLen = len(self.path)
                changeSight = True
                if (self.forward):
                    self.nextTile += 1
                else:
                    self.nextTile -= 1
                if (self.rotate):
                    self.nextTile = (self.nextTile + pathLen) % pathLen
                else:
                    if (self.nextTile < 0 or self.nextTile >= pathLen):
                        if (self.nextTile < 0):
                            self.nextTile = 1
                        if (self.nextTile >= pathLen):
                            self.nextTile = pathLen - 2
                        self.stayTime = 1000
                        self.state = "stay"
                        self.forward = not self.forward
                        changeSight = False
                if (changeSight):
                    nextXN, nextYN = self.path[self.nextTile]
                    if (abs(nextXN - nextX) == 0):
                        self.setSightDir("down" if nextYN > nextY else "up")
                    else:
                        self.setSightDir("right" if nextXN > nextX else "left")
            else:
                if (dx > 0):
                    self.animator.setAnimation("moveD")
                elif (dx < 0):
                    self.animator.setAnimation("moveA")
            a = math.atan2(dy, dx)
            self.speedX = math.cos(a) * self.speed
            self.speedY = math.sin(a) * self.speed
            if (abs(dx) < self.speed):
                self.speedX = dx
            if (abs(dy) < self.speed):
                self.speedY = dy
            if (self.checkPlayer()):
                self.state = "attack"
                self.startPos = (int(self.x), int(self.y))
        elif (self.state == "attack"):
            self.sightZoneVisible = False
            dx = (self.screen.player.x + self.screen.player.width / 2) - (self.x + self.width / 2)
            dy = (self.screen.player.y + self.screen.player.height / 2) - (self.y + self.height / 2)
            a = math.atan2(dy, dx)
            self.speedX = math.cos(a) * self.speed
            self.speedY = math.sin(a) * self.speed

    def checkPlayer(self):
        seeSpeed = 0.001
        unseeSpeed = 0.0002
        if (not self.screen.player.visibleForEnemies):
            self.seePlayer = max(self.seePlayer - unseeSpeed * 1000 / Settings.fps, 0)
            return False
        dx = (self.screen.player.x + self.screen.player.width / 2) - (self.x + self.width / 2)
        dy = (self.screen.player.y + self.screen.player.height / 2) - (self.y + self.height / 2)
        distance = dx * dx + dy * dy
        if (distance > self.lookR ** 2):
            self.seePlayer = max(self.seePlayer - unseeSpeed * 1000 / Settings.fps, 0)
            return False
        a = math.atan2(dy, dx) % (2 * math.pi)
        betweenA = abs(self.sightDirCur - a)
        betweenA = min((2 * math.pi) - betweenA, betweenA)
        if (betweenA <= math.pi / 4):
            self.seePlayer = min(self.seePlayer + seeSpeed * 1000 / Settings.fps, 1)
            return self.seePlayer >= distance / self.lookR ** 2
        else:
            self.seePlayer = max(self.seePlayer - unseeSpeed * 1000 / Settings.fps, 0)
        return False

    def setSightDir(self, dir: Union[Literal["up"], Literal["right"], Literal["down"], Literal["left"]]):
        if (dir == "right"):
            self.sightDir = 0
            self.sightDirCur = 0
        elif (dir == "down"):
            self.sightDir = 90 / 180 * math.pi
            self.sightDirCur = 90 / 180 * math.pi
        elif (dir == "left"):
            self.sightDir = 180 / 180 * math.pi
            self.sightDirCur = 180 / 180 * math.pi
        elif (dir == "up"):
            self.sightDir = 270 / 180 * math.pi
            self.sightDirCur = 270 / 180 * math.pi


EntityAlive.registerEntity("aborigine", EntityAborigine)
