import math
from random import randint
from typing import Any, Callable, Literal, Union
import pygame
from functions import drawPie
from game.animator import Animator, AnimatorData
from game.entity import EntityAlive, EntityGroups
from game.pathFinder import PathFinder
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
SPEED_PATROL = 0.05
SPEED_SURROUND = 0.1
SPEED_SEARCH = 0.03


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
        self.pathFinder = PathFinder(self)
        self.group = EntityGroups.enemy
        self.speed = SPEED_PATROL
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
        self.targetPast = (0, 0)
        self.searchTime = 0
        self.searchCounter = 0
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
            if (EntityAborigine.Leader == self):
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
            if (self.pathFinder._target):
                x, y = self.pathFinder._target
                pygame.draw.circle(surface, "blue", (x * Settings.tileSize, y * Settings.tileSize), 4)
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
        collisions = super().update()
        if (not self.alive or Settings.disableAI):
            return

        if (self.state == "stay"):
            self.sightZoneVisible = True
            self.speedX = 0
            self.speedY = 0
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
            self.sightZoneVisible = True
            self.speed = SPEED_PATROL
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
                self.setDirection(dx, dy)
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
        elif (self.state == "surround"):
            self.speed = SPEED_SURROUND
            self.sightZoneVisible = False
            dx = (self.screen.player.x + self.screen.player.width / 2) - (self.x + self.width / 2)
            dy = (self.screen.player.y + self.screen.player.height / 2) - (self.y + self.height / 2)
            if (self.screen.player.visibleForEnemies or (abs(dx) < 1.5 and abs(dy) < 1.5)):
                self.targetPast = (self.target[0] * self.screen.player.width + self.screen.player.x,
                                   self.target[1] * self.screen.player.height + self.screen.player.y)
                self.pathFinder.setTragetEntity(self.screen.player,
                                                self.target[0] * self.screen.player.width,
                                                self.target[1] * self.screen.player.height)
            else:
                self.pathFinder.setTragetCoord(self.targetPast[0], self.targetPast[1])
            self.pathFinder.apllySpeed()
            if (self.speedY == 0 and self.speedX == 0):
                self.animator.setAnimation("stay" + self.direction)
                if (not (self.screen.player.visibleForEnemies or (abs(dx) < 1.5 and abs(dy) < 1.5))):
                    self.state = "search"
                    self.searchTime = 0
                    self.searchCounter = 0
            else:
                self.setDirection(self.speedX, self.speedY)
                self.animator.setAnimation("move" + self.direction)
            if (abs(dx) < 0.9 and abs(dy) < 0.9):
                self.state = "hit"
                self.speedX = 0
                self.speedY = 0
                self.setDirection(dx, dy)
                self.animator.setAnimation("attack" + self.direction)
        elif (self.state == "hit"):
            if (self.animator.lastState[1]):
                self.state = "surround"
                self.animator.setAnimation("stay" + self.direction)
        elif (self.state == "search"):
            self.sightZoneVisible = True
            self.speed = SPEED_SEARCH
            self.searchTime -= 1000 / Settings.fps
            if (self.searchTime <= 0):
                self.searchCounter += 1
                self.searchTime = 500
                a = randint(0, 360) / 180 * math.pi
                self.speedX = math.cos(a) * self.speed
                self.speedY = math.sin(a) * self.speed
                self.setDirection(self.speedX, self.speedY)
                self.animator.setAnimation("move" + self.direction)
                if (self.searchCounter >= 8):
                    self.state = "return"
        elif (self.state == "return"):
            self.sightZoneVisible = True
            self.speed = SPEED_PATROL
            self.pathFinder.setTragetCoord(self.startPos[0] + 0.5, self.startPos[1] + 0.5)
            self.pathFinder.apllySpeed()
            self.setDirection(self.speedX, self.speedY)
            self.animator.setAnimation("move" + self.direction)
            if (int(self.x) == self.startPos[0] and int(self.y) == self.startPos[1]):
                self.state = "stay"
                self.animator.setAnimation("stay" + self.direction)


    def setDirection(self, x, y):
        if (abs(y) > abs(x)):
            if (y > 0):
                self.direction = "S"
            elif (y < 0):
                self.direction = "W"
        else:
            if (x > 0):
                self.direction = "D"
            elif (x < 0):
                self.direction = "A"

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
        EntityAborigine.Leader = self
        self.allies = list(filter(lambda e: e.id == self.id, self.screen.entities))
        if (len(self.allies) == 1):
            self.allies[0].startAttack((0, 0))
            return
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
        self.state = "surround"
        self.target = target
        self.startPos = (int(self.x), int(self.y))


EntityAlive.registerEntity("aborigine", EntityAborigine)
