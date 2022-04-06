import math
from random import choice, randint
from typing import Any, Callable
import pygame
from game.animator import Animator, AnimatorData
from game.entity import EntityAlive, EntityGroups
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("tentacle", [
    ("stay.png", 0, (16, 16), (-0.25, -0.0625, 1, 1)),
    ("appear.png", 300, (16, 16), (-0.25, -0.0625, 1, 1)),
    ("attack.png", 300, (16, 16), (-0.25, -0.0625, 1, 1)),
    ("hide.png", 300, (16, 16), (-0.25, -0.0625, 1, 1)),
])


class EntityTentacle(EntityAlive):
    def __init__(self, screen, data: dict = None):
        self.appearCells = []
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.group = EntityGroups.enemy
        self.ghostE = True
        self.strength = 1
        self.healthMax = 3
        self.health = 3
        self.width = 0.5
        self.height = 0.9375
        self.visible = False
        self.hidden = True
        self.counter = randint(3, 6) * 500
        self.state = "hidden"

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        if ("appearCells" in data and data["appearCells"] is not None):
            self.appearCells = data["appearCells"]
        else:
            self.appearCells = self.getWaterCells()

    def draw(self, surface: pygame.Surface):
        if (self.visible):
            super().draw(surface)
        else:
            self.draw_dev(surface)

    def canGoOn(self, tile: Tile) -> bool:
        return "water-deep" in tile.tags or super().canGoOn(tile)

    def update(self):
        super().update()
        if (not self.alive or Settings.disableAI):
            return
        self.counter -= 1000 / Settings.fps
        if (self.state == "hidden"):
            if (self.counter <= 0):
                self.animator.setAnimation("appear")
                self.visible = True
                self.hidden = False
                self.strength = 1
                self.state = "appear"
                x, y = choice(self.appearCells)
                self.x = x + (1 - self.width) / 2
                self.y = y + (1 - self.height) / 2
        elif (self.state == "appear"):
            if (self.animator.lastState[1]):
                if (self.screen.player.visibleForEnemies):
                    self.animator.setAnimation("attack")
                    self.state = "attack"
                else:
                    self.animator.setAnimation("hide")
                    self.state = "hide"
        elif (self.state == "attack"):
            if (self.animator.lastState[0] and self.animator.frame == 2):
                self.fire()
            if (self.animator.lastState[1]):
                self.counter = 1000
                self.animator.setAnimation("stay")
                self.state = "stay"
        elif (self.state == "stay"):
            if (self.counter <= 0):
                self.animator.setAnimation("hide")
                self.state = "hide"
        elif (self.state == "hide"):
            if (self.animator.lastState[1]):
                self.animator.setAnimation("stay")
                self.state = "hidden"
                self.visible = False
                self.hidden = True
                self.strength = 0
                self.counter = randint(3, 6) * 500

    def getWaterCells(self):
        cells = []
        for tile, x, y in self.screen.getTiles():
            if ("water-deep" in tile.tags):
                cells.append((x, y))
        return cells

    def fire(self):
        ball = EntityAlive.createById("ink", self.screen)
        ball.x = self.x + self.width - ball.width
        ball.y = self.y
        dx = (self.screen.player.x + self.screen.player.width / 2) - (ball.x + ball.width / 2)
        dy = (self.screen.player.y + self.screen.player.height / 2) - (ball.y + ball.height / 2)
        a = math.atan2(dy, dx)
        ball.speedX = math.cos(a) * ball.speed
        ball.speedY = math.sin(a) * ball.speed
        self.screen.addEntity(ball)


EntityAlive.registerEntity("tentacle", EntityTentacle)
