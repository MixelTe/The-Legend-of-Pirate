import math
from game.entity import Entity
from settings import Settings


class PathFinder:
    def __init__(self, entity: Entity):
        self._entity = entity
        self._targetEntity: Entity = None
        self._target = None
        self._curTile = None

    def setTragetCoord(self, x: float, y: float):
        self._target = (x, y)

    def setTragetEntity(self, entity, dx: float = 0, dy: float = 0):
        self._target = (dx, dy)
        self._targetEntity = entity

    def apllySpeed(self) -> bool:
        if (self._targetEntity):
            tx = self._targetEntity.x + self._targetEntity.width / 2 + self._target[0]
            ty = self._targetEntity.y + self._targetEntity.height / 2 + self._target[1]
        else:
            tx, ty = self._target
        if (self._curTile is None):
            self._curTile = (int(self._entity.x + self._entity.width / 2), int(self._entity.y + self._entity.height / 2))
        path = self._findPath(self._curTile[0], self._curTile[1], int(tx), int(ty))
        if (not path):
            self._entity.speedY = 0
            self._entity.speedX = 0
            if (self._targetEntity):
                tx = self._targetEntity.x + self._targetEntity.width / 2
                ty = self._targetEntity.y + self._targetEntity.height / 2
                path = self._findPath(self._curTile[0], self._curTile[1], int(tx), int(ty))
                if (not path):
                    return False
            else:
                return False
        nextX = path[-2][0] + (1 - self._entity.width) / 2
        nextY = path[-2][1] + (1 - self._entity.height) / 2
        dx = nextX - self._entity.x
        dy = nextY - self._entity.y
        a = math.atan2(dy, dx)
        self._entity.speedX = math.cos(a) * self._entity.speed
        self._entity.speedY = math.sin(a) * self._entity.speed
        if (abs(dx) < self._entity.speed):
            self._entity.speedX = 0
            self._entity.x = nextX
        if (abs(dy) < self._entity.speed):
            self._entity.speedY = 0
            self._entity.y = nextY
        if (self._entity.speedY == 0 and self._entity.speedX == 0):
            self._curTile = (int(self._entity.x + self._entity.width / 2), int(self._entity.y + self._entity.height / 2))
        return self._entity.x == tx and self._entity.y == ty

    def _findPath(self, x1, y1, x2, y2):
        field = []
        for y in range(Settings.screen_height):
            row = []
            field.append(row)
            for x in range(Settings.screen_width):
                tile = self._entity.screen.tiles[y][x]
                if (self._entity.canGoOn(tile)):
                    row.append(-1)
                else:
                    row.append(None)

        # for entity in self._entity.screen.entities:
        #     rect = entity.get_rect()
        #     x =

        field[y1][x1] = 0
        d = 0
        found = False
        while not found:
            changedOne = False
            for y in range(Settings.screen_height):
                for x in range(Settings.screen_width):
                    if (field[y][x] == d):
                        for Y in range(y - 1, y + 2):
                            for X in range(x - 1, x + 2):
                                if (X >= 0 and X < Settings.screen_width and Y >= 0 and Y < Settings.screen_height
                                        and (x == X or y == Y) and field[Y][X] == -1):
                                    field[Y][X] = d + 1
                                    changedOne = True
                                    if (X == x2 and Y == y2):
                                        found = True
            if (not changedOne):
                break
            d += 1

        if (not found):
            return False

        d = field[y2][x2]
        path = [(x2, y2)]
        while d >= 0:
            x, y = path[-1]
            found = False
            for Y in range(y - 1, y + 2):
                for X in range(x - 1, x + 2):
                    if (X >= 0 and X < Settings.screen_width and Y >= 0 and Y < Settings.screen_height
                            and (x == X or y == Y)):
                        if (field[Y][X] == d - 1):
                            path.append((X, Y))
                            found = True
                            break
                if (found):
                    break
            d -= 1
        return path
