import math
from typing import Any, Callable, Literal, Union

import pygame
from functions import drawPie, dropCoin
from game.animator import Animator, AnimatorData
from game.entities.aborigine import EntityAborigine
from game.entity import Entity, EntityAlive, EntityGroups
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("aborigineBow", [
    ("stay.png", 0, (15, 16), (-0.4, -0.6, 1.2, 1.3)),
    ("stayA.png", 0, (15, 16), (-0.4, -0.6, 1.2, 1.3)),
    ("stayD.png", 0, (15, 16), (-0.4, -0.6, 1.2, 1.3)),
    ("attackD.png", 200, (15, 16), (-0.4, -0.6, 1.2, 1.3)),
    ("attackA.png", 200, (15, 16), (-0.4, -0.6, 1.2, 1.3)),
])
LOOKR = 5


class EntityAborigineBow(EntityAlive):
    def __init__(self, screen, data: dict = None):
        self.direction = "D"
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.group = EntityGroups.enemy
        self.strength = 1
        self.healthMax = 2
        self.health = 2
        self.width = 0.32
        self.height = 0.7
        self.startPos = (int(self.x), int(self.y))
        self.state = "stay"
        self.dirRight = True
        self.sightDirCur = 0
        self.lookR = LOOKR
        self.sightZoneVisible = True
        self.seePlayer = 0
        self.rotationSpeed = 0.01 * 1.5
        self.setSightDir()

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        if ("direction" in data):
            if (data["direction"] == "right"):
                self.direction = "D"
            if (data["direction"] == "left"):
                self.direction = "A"
            if (data["direction"] == "up"):
                self.direction = "W"
            if (data["direction"] == "down"):
                self.direction = "S"

    def canGoOn(self, tile: Tile) -> bool:
        return "water" not in tile.tags and super().canGoOn(tile)

    def canPassThrough(self, entity: Entity) -> bool:
        return entity.id == "arrow"

    def onDeath(self):
        dropCoin()

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

    def update(self):
        super().update()
        if (not self.alive or Settings.disableAI):
            return

        self.speedX = min(0.08, self.startPos[0] + (1 - self.width) / 2 - self.x)
        self.speedY = min(0.08, self.startPos[1] + (1 - self.height) / 2 - self.y)

        if (self.state == "stay"):
            self.animator.setAnimation("stay" + self.getDir())
            self.sightZoneVisible = True
            if (self.checkPlayer()):
                self.alertAlly()
                self.state = "attack"
                self.sightZoneVisible = False
                self.animator.setAnimation("attack" + self.getDir())
            else:
                self.sightDirCur += self.rotationSpeed
                if (abs(self.sightDirCur - self.sightDir) > 60 / 180 * math.pi):
                    self.rotationSpeed *= -1
        elif (self.state == "attack"):
            self.sightZoneVisible = False
            if (self.animator.lastState[1]):
                self.state = "stay"
                self.shoot()

    def setSightDir(self, dir: Union[Literal["W"], Literal["D"], Literal["S"], Literal["A"], Literal[None]] = None):
        if (dir is None):
            dir = self.direction
        if (dir == "D"):
            self.sightDir = 0
            self.sightDirCur = 0
        elif (dir == "S"):
            self.sightDir = 90 / 180 * math.pi
            self.sightDirCur = 90 / 180 * math.pi
        elif (dir == "A"):
            self.sightDir = 180 / 180 * math.pi
            self.sightDirCur = 180 / 180 * math.pi
        elif (dir == "W"):
            self.sightDir = 270 / 180 * math.pi
            self.sightDirCur = 270 / 180 * math.pi

    def getDir(self):
        if (self.direction == "D" or self.direction == "S"):
            return "D"
        if (self.direction == "A" or self.direction == "W"):
            return "A"

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

    def alertAlly(self):
        for entity in self.screen.entities:
            if (isinstance(entity, EntityAborigine)):
                entity.startAttackAsLeader()
                return

    def shoot(self):
        arrow = EntityAlive.createById("arrow", self.screen)
        arrow.x = self.x + self.width - arrow.width
        arrow.y = self.y
        dx = (self.screen.player.x + self.screen.player.width / 2) - (arrow.x + arrow.width / 2)
        dy = (self.screen.player.y + self.screen.player.height / 2) - (arrow.y + arrow.height / 2)
        a = math.atan2(dy, dx)
        arrow.speedX = math.cos(a) * arrow.speed
        arrow.speedY = math.sin(a) * arrow.speed
        self.screen.addEntity(arrow)


EntityAlive.registerEntity("aborigineBow", EntityAborigineBow)
