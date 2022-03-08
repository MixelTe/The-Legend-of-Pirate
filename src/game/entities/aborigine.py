import math
from typing import Any, Callable, Literal, Union
import pygame
from functions import drawPie
from game.animator import Animator, AnimatorData
from game.entity import EntityAlive, EntityGroups
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("aborigine", [
    ("stayW.png", 0, (15, 16), (-0.591, -0.6, 1.2, 1.3)),
    ("stayS.png", 0, (15, 16), (-0.241, -0.6, 1.2, 1.3)),
    ("stayA.png", 0, (15, 16), (-0.591, -0.6, 1.2, 1.3)),
    ("stayD.png", 0, (15, 16), (-0.241, -0.6, 1.2, 1.3)),
    ("moveW.png", 150, (15, 16), (-0.591, -0.6, 1.2, 1.3)),
    ("moveS.png", 150, (15, 16), (-0.241, -0.6, 1.2, 1.3)),
    ("moveA.png", 150, (15, 16), (-0.591, -0.6, 1.2, 1.3)),
    ("moveD.png", 150, (15, 16), (-0.241, -0.6, 1.2, 1.3)),
    ("attackW.png", 200, (15, 16), (-0.591, -0.6, 1.2, 1.3)),
    ("attackS.png", 200, (15, 18), (-0.241, -0.6, 1.2, 1.46)),
    ("attackA.png", 200, (16, 16), (-0.68, -0.6, 1.3, 1.3)),
    ("attackD.png", 200, (16, 16), (-0.241, -0.6, 1.3, 1.3)),
])
LOOKR = 4


class EntityAborigine(EntityAlive):
    Leader = None

    def __init__(self, screen, data: dict = None):
        self.type = "stay"  # stay, patrol
        self.rotate = False
        self.path = []
        self.direction = "D"
        self.rotationSpeed = 0.01
        super().__init__(screen, data)
        self.startPos = (int(self.x), int(self.y))
        self.animator = Animator(animatorData, "stayD")
        self.group = EntityGroups.enemy
        self.speed = 0.05
        self.strength = 0
        self.healthMax = 2
        self.health = 2
        self.width = 0.32
        self.height = 0.7
        self.state = "stay"
        self.sightDir = 0
        self.sightDirCur = 0
        self.nextTile = 1
        self.lookR = LOOKR
        self.forward = True
        self.seePlayer = 0
        self.sightZoneVisible = True
        self.stayTime = 0
        self.allies = []
        self.target = (0, 0)
        self.setSightDir()
        self.animator.setAnimation("attackS")

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        dataSetter("type", self.type)
        dataSetter("rotate", self.rotate)
        if ("direction" in data):
            if (data["direction"] == "right"):
                self.direction = "D"
            if (data["direction"] == "left"):
                self.direction = "A"
            if (data["direction"] == "up"):
                self.direction = "W"
            if (data["direction"] == "down"):
                self.direction = "S"
        if self.rotate:
            self.rotationSpeed *= 1.5
        dataSetter("path", self.path)
        if (self.path and len(self.path) <= 1):
            self.type = "stay"

    def canGoOn(self, tile: Tile) -> bool:
        return "water" not in tile.tags and super().canGoOn(tile)

    def onDeath(self):
        coin = EntityAlive.createById("coin", self.screen)
        self.screen.addEntity(coin)
        coin.x = self.x + self.width / 2
        coin.y = self.y + self.height / 2

    def draw(self, surface: pygame.Surface, opaque=1):
        super().draw(surface, opaque)
        if (Settings.drawHitboxes):
            if (self.leader):
                points = [
                    (0, 0),
                    (0.4, 0),
                    (0.3, 0.1),
                    (0.4, 0.2),
                    (0, 0.2),
                ]
                points = [((self.x + p[0]) * Settings.tileSize, (self.y + p[1] - 0.4) * Settings.tileSize) for p in points]
                pygame.draw.polygon(surface, "red", points)
        x = (self.screen.player.x + self.screen.player.width * (0.5 + self.target[0])) * Settings.tileSize
        y = (self.screen.player.y + self.screen.player.height * (0.5 + self.target[1])) * Settings.tileSize
        pygame.draw.circle(surface, "red", (x, y), 2)
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
            self.animator.setAnimation("stay" + self.direction)
            if (self.type == "patrol"):
                if (self.stayTime <= 0):
                    self.state = "patrol"
                    nextX, nextY = self.path[self.nextTile]
                    if (abs(int(self.x) - nextX) == 0):
                        self.direction = "S" if int(self.y) < nextY else "W"
                    else:
                        self.direction = "D" if int(self.x) < nextX else "A"
                    self.animator.setAnimation("move" + self.direction)
                    self.setSightDir()
            self.sightDirCur += self.rotationSpeed
            maxR = 60 if self.rotate else 20
            if (abs(self.sightDirCur - self.sightDir) > maxR / 180 * math.pi):
                self.rotationSpeed *= -1
            if (self.checkPlayer()):
                self.startAttackAsLeader()
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
                        self.direction = "S" if nextYN > nextY else "W"
                    else:
                        self.direction = "D" if nextXN > nextX else "A"
                    self.setSightDir()
            else:
                if (abs(dy) > abs(dx)):
                    if (dy > 0):
                        self.direction = "S"
                    elif (dy < 0):
                        self.direction = "W"
                else:
                    if (dx > 0):
                        self.direction = "D"
                    elif (dx < 0):
                        self.direction = "A"
                self.animator.setAnimation("move" + self.direction)
            a = math.atan2(dy, dx)
            self.speedX = math.cos(a) * self.speed
            self.speedY = math.sin(a) * self.speed
            if (abs(dx) < self.speed):
                self.speedX = dx
            if (abs(dy) < self.speed):
                self.speedY = dy
            if (self.checkPlayer()):
                self.startAttackAsLeader()
        elif (self.state == "attack"):
            self.sightZoneVisible = False
            tx = (self.screen.player.x + self.screen.player.width * (0.5 + self.target[0])) - self.width / 2
            ty = (self.screen.player.y + self.screen.player.height * (0.5 + self.target[1])) - self.height / 2
            dx = tx - self.x
            dy = ty - self.y
            a = math.atan2(dy, dx)
            self.speedX = math.cos(a) * self.speed
            self.speedY = math.sin(a) * self.speed
            if (abs(dx) < self.speed):
                self.speedX = 0
                self.x = tx
            if (abs(dy) < self.speed):
                self.speedY = 0
                self.y = ty

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

    def startAttackAsLeader(self):
        self.state = "attack"
        self.startPos = (int(self.x), int(self.y))
        EntityAborigine.Leader = self
        self.allies = list(filter(lambda e: e.id == self.id, self.screen.entities))
        positions = [[[] for _ in range(3)] for _ in range(3)]
        px, py, pw, ph = self.screen.player.x, self.screen.player.x, self.screen.player.width, self.screen.player.height
        def distance(ally, dx, dy):
            dX = ally.x - (px + dx)
            dY = ally.y - (py + dy)
            dis = dX ** 2 + dY ** 2
            if ((dx < 0 and dX > 0) or (dx > 0 and dX < 0)):
                dis *= 100
            if ((dy < 0 and dY > 0) or (dy > 0 and dY < 0)):
                dis *= 100
            return dis
        for i, ally in enumerate(self.allies):
            for y in range(3):
                for x in range(3):
                    positions[y][x].append((i, distance(ally, (x - 1) * pw, (y - 1) * ph)))

        sent = []
        def sendAlly(x, y):
            ways = positions[y + 1][x + 1]
            ways.sort(key=lambda el: el[1])
            for way in ways:
                i, distance = way
                if (i not in sent):
                    sent.append(i)
                    self.allies[i].startAttack((x * 1.1, y * 1.1))
                    return
        sendAlly(1, 0)
        sendAlly(-1, 0)
        sendAlly(0, 1)
        sendAlly(0, -1)
        sendAlly(1, 1)
        sendAlly(1, -1)
        sendAlly(-1, 1)
        sendAlly(-1, -1)

        for i, ally in enumerate(self.allies):
            if (i not in sent):
                ally.startAttack()

    def startAttack(self, target=(0, 0)):
        self.state = "attack"
        self.target = target
        self.startPos = (int(self.x), int(self.y))



EntityAlive.registerEntity("aborigine", EntityAborigine)
