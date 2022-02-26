import math
from typing import Any, Callable

import pygame
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
        self.lookDir = 0
        super().__init__(screen, data)
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
        self.forward = True

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        dataSetter("type", self.type)
        dataSetter("rotate", self.rotate)
        dataSetter("path", self.path)
        if (self.path and len(self.path) <= 1):
            self.type = "stay"
        if ("direction" in data):
            if (data["direction"] == "right"):
                self.lookDir = 0
            elif (data["direction"] == "down"):
                self.lookDir = 90 / 180 * math.pi
            elif (data["direction"] == "left"):
                self.lookDir = 180 / 180 * math.pi
            elif (data["direction"] == "up"):
                self.lookDir = 270 / 180 * math.pi

    def canGoOn(self, tile: Tile) -> bool:
        return "water" not in tile.tags and super().canGoOn(tile)

    def onDeath(self):
        coin = EntityAlive.createById("coin", self.screen)
        self.screen.addEntity(coin)
        coin.x = self.x + self.width / 2
        coin.y = self.y + self.height / 2

    def draw_dev(self, surface: pygame.Surface):
        super().draw_dev(surface)
        if (Settings.drawHitboxes):
            p1 = (self.x * Settings.tileSize, self.y * Settings.tileSize)
            p2 = (self.x * Settings.tileSize + math.cos(self.lookDir) * 4 * Settings.tileSize,
                  self.y * Settings.tileSize + math.sin(self.lookDir) * 4 * Settings.tileSize)
            pygame.draw.line(surface, "orange", p1, p2)

    def update(self):
        super().update()
        if (not self.alive or Settings.disableAI):
            return

        if (self.state == "stay"):
            if (self.type == "patrol"):
                self.state = "patrol"
                self.animator.setAnimation("moveA")
        elif (self.state == "patrol"):
            nextX, nextY = self.path[self.nextTile]
            dx = (nextX + 0.5) - (self.x + self.width / 2)
            dy = (nextY + 0.5) - (self.y + self.height / 2)
            if (abs(dx) <= 0.01 and abs(dy) <= 0.01):
                pathLen = len(self.path)
                if (self.forward):
                    self.nextTile += 1
                else:
                    self.nextTile -= 1
                if (self.rotate):
                    self.nextTile = (self.nextTile + pathLen) % pathLen
                else:
                    if (self.nextTile < 0):
                        self.forward = not self.forward
                        self.nextTile = 1
                    if (self.nextTile >= pathLen):
                        self.forward = not self.forward
                        self.nextTile = pathLen - 2
            else:
                if (dx > 0):
                    self.animator.setAnimation("moveD")
                elif (dx < 0):
                    self.animator.setAnimation("moveA")
            a = math.atan2(dy, dx)
            self.speedX = math.cos(a) * self.speed
            self.speedY = math.sin(a) * self.speed


EntityAlive.registerEntity("aborigine", EntityAborigine)
