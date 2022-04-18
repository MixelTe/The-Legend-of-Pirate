import math
from typing import Any, Callable, Union
import pygame
from backMusic import endBattleMusic, startBattleMusic
from functions import joinPath
from game.animator import Animator, AnimatorData
from game.decor import Decor
from game.entity import Entity, EntityAlive, EntityGroups
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("octopus", [
    ("stay.png", 300, (32, 32), (0, 0, 2, 2)),
    ("hit.png", 800, (32, 32), (0, 0, 2, 2)),
    ("appear.png", 100, (32, 32), (0, 0, 2, 2)),
    ("hide.png", 100, (32, 32), (0, 0, 2, 2)),
])

battleMusic = (
    joinPath(Settings.folder_data, Settings.folder_sounds, "bossBattle", "bossBattle_start.mp3"),
    joinPath(Settings.folder_data, Settings.folder_sounds, "bossBattle", "bossBattle.mp3"),
    joinPath(Settings.folder_data, Settings.folder_sounds, "bossBattle", "bossBattle_end.mp3"),
    1
)
font = pygame.font.Font(Settings.path_font, int(Settings.tileSize * 1.2))


class EntityOctopus(EntityAlive):
    def __init__(self, screen, data: dict = None):
        self.entrance = [(19, 3), (19, 4), (19, 5)]
        self.exit = [(0, 3), (0, 4), (0, 5)]
        self.startZone = [2, 2, 16, 5]
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.group = EntityGroups.enemy
        self.removeOnDeath = False
        self.attackPushback = False
        self.strength = 0
        self.healthMax = 9
        self.health = 9
        self.width = 2
        self.height = 2
        self.x = (Settings.screen_width - self.width) / 2
        self.y = (Settings.screen_height - self.height) / 2
        self.state = "hidden"
        self.attackCount = 0
        self.visible = False
        self.settedDecor = []
        self.tentacles = []
        self.dev_zones = []
        self.counter = 0
        if ("octopus-defeated" not in self.screen.saveData.tags):
            self.blockTiles(self.exit)
            self.state = "awaitStart"

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        dataSetter("entrance", self.entrance)
        dataSetter("exit", self.exit)
        dataSetter("startZone", self.startZone)

    def draw(self, surface: pygame.Surface, opaque=1):
        if (self.visible):
            super().draw(surface, opaque)

        if (Settings.drawHitboxes and False):
            for i, zone in enumerate(self.dev_zones):
                color = pygame.Color(0, 0, 0)
                color.hsla = ((i * (360 / len(self.dev_zones)) * 2) % 360, 100, 50, 100)
                for x, y in zone:
                    pygame.draw.rect(surface, color, [x * Settings.tileSize, y * Settings.tileSize, Settings.tileSize, Settings.tileSize], 3)

        if (Settings.drawHitboxes):
            text = font.render(f"{self.health}", True, "red")
            surface.blit(text, (self.x * Settings.tileSize, self.y * Settings.tileSize))

    def canGoOn(self, tile: Tile) -> bool:
        return super().canGoOn(tile)

    def onDeath(self):
        coin = EntityAlive.createById("coin", self.screen)
        self.screen.addEntity(coin)
        coin.x = self.x + self.width / 2
        coin.y = self.y + self.height / 2

    def update(self):
        super().update()
        if (Settings.disableAI):
            return

        self.counter = max(0, self.counter - 1000 / Settings.fps)
        if (self.state == "hidden"):
            self.visible = False
            self.immortal = True
        elif (self.state == "awaitStart"):
            self.visible = False
            self.immortal = True
            if (self.screen.player.is_inRect(self.startZone)):
                self.state = "startAppear"
                self.animator.setAnimation("appear")
                self.blockTiles(self.entrance)
                startBattleMusic(*battleMusic)
                self.x = (Settings.screen_width - self.width) / 2
                self.y = (Settings.screen_height - self.height) / 2
        elif (self.state == "startAppear"):
            self.visible = True
            self.immortal = True
            if (self.animator.lastState[1]):
                self.state = "startStay"
                self.animator.setAnimation("stay")
                self.counter = 3000
        elif (self.state == "startStay"):
            self.visible = True
            self.immortal = True
            if (self.counter <= 0):
                self.state = "startHide"
                self.animator.setAnimation("hide")
        elif (self.state == "startHide"):
            self.visible = True
            self.immortal = True
            if (self.animator.lastState[1]):
                self.visible = False
                self.state = "start"
                self.animator.setAnimation("stay")
        elif (self.state == "start"):
            self.visible = False
            self.immortal = True
            if (self.health <= 0):
                self.endBattle()
            else:
                self.createTentacles(3 + (3 - self.health // 3))
                self.state = "tentacle"
        elif (self.state == "tentacle"):
            self.visible = False
            self.immortal = True
            self.tentacles = list(filter(lambda el: el.alive, self.tentacles))
            if (len(self.tentacles) == 0):
                self.state = "appear"
                self.visible = True
                self.animator.setAnimation("appear")
                self.x = (Settings.screen_width - self.width) / 2
                self.y = (Settings.screen_height - self.height) / 2
                self.attackCount = 0
        elif (self.state == "appear"):
            self.visible = True
            self.immortal = True
            if (self.animator.lastState[1]):
                self.animator.setAnimation("stay")
                self.state = "visible"
        elif (self.state == "visible"):
            self.animator.setAnimation("stay")
            self.visible = True
            self.immortal = False
        elif (self.state == "hit"):
            self.visible = True
            self.immortal = True
            if (self.animator.lastState[1]):
                if (self.attackCount >= 3):
                    self.state = "hide"
                    self.animator.setAnimation("hide")
                else:
                    self.state = "visible"
                    self.animator.setAnimation("stay")
        elif (self.state == "hide"):
            self.visible = True
            self.immortal = True
            if (self.animator.lastState[1]):
                self.visible = False
                self.animator.setAnimation("stay")
                self.state = "start"

        self.hidden = not self.visible

    def takeDamage(self, damage: int, attacker: Union[Entity, str, None] = None):
        if (super().takeDamage(damage, attacker)):
            self.attackCount += 1
            self.immortal = True
            self.state = "hit"
            self.animator.setAnimation("hit")

    def blockTiles(self, tiles: list[tuple[int, int]]):
        def setDecor(x, y, tx, ty):
            if (x >= 0 and x < Settings.screen_width and y >= 0 and y < Settings.screen_height):
                if (self.screen.tiles[y][x].id == "water_deep"):
                    return
                for X, Y in tiles:
                    if (X == x and Y == y):
                        return
                sides = [False, False, False, False]  # top, right, bottom, left
                if (tx < x):
                    sides[3] = True
                if (tx > x):
                    sides[1] = True
                if (ty < y):
                    sides[0] = True
                if (ty > y):
                    sides[2] = True
                decor = Decor.fromData({"className": "tileEdge_water_deep", "x": x, "y": y, "sides": sides})
                self.screen.decor.append(decor)
                self.settedDecor.append(decor)
        for x, y in tiles:
            self.screen.tiles[y][x] = Tile.fromId("water_deep")
            setDecor(x - 1, y, x, y)
            setDecor(x + 1, y, x, y)
            setDecor(x, y - 1, x, y)
            setDecor(x, y + 1, x, y)

    def unblockTiles(self, tiles: list[tuple[int, int]]):
        for x, y in tiles:
            self.screen.tiles[y][x] = Tile.fromId("water_low")

    def createTentacles(self, count):
        step = 2 * math.pi / count
        center = (Settings.screen_width // 2, Settings.screen_height // 2)
        self.dev_zones = []
        for i in range(count):
            tiles = []
            for y in range(Settings.screen_height):
                for x in range(Settings.screen_width):
                    if ((x == center[0] and y == center[1]) or
                        (x == center[0] - 1 and y == center[1]) or
                        (x == center[0] and y == center[1] - 1) or
                        (x == center[0] - 1 and y == center[1] - 1) or
                        (x == center[0] and y == center[1] + 1) or
                            (x == center[0] - 1 and y == center[1] + 1)):
                        continue
                    a = math.atan2(y - center[1], x - center[0]) % (2 * math.pi)
                    betweenA = abs(i * step - a)
                    betweenA = min((2 * math.pi) - betweenA, betweenA)
                    if (betweenA <= step / 2):
                        tiles.append((x, y))
            tentacle = Entity.createById("tentacle", self.screen)
            tentacle.appearCells = tiles
            self.screen.addEntity(tentacle)
            self.tentacles.append(tentacle)
            self.dev_zones.append(tiles)

    def endBattle(self):
        self.state = "hidden"
        self.visible = False
        self.immortal = True
        endBattleMusic(True)
        self.unblockTiles(self.entrance)
        self.unblockTiles(self.exit)
        for decor in self.settedDecor:
            self.screen.decor.remove(decor)
        self.screen.saveData.tags.append("octopus-defeated")

EntityAlive.registerEntity("octopus", EntityOctopus)
