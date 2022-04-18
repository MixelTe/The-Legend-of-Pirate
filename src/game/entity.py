from __future__ import annotations
from typing import Any, Callable, Union
import pygame
from functions import GameExeption, load_sound, multRect, rectIntersection
from game.animator import Animator
from game.tile import Tile
from settings import Settings


screenBorders = [
    (-1, 0, 1, Settings.screen_height),
    (Settings.screen_width, 0, 1, Settings.screen_height),
    (0, -1, Settings.screen_width, 1),
    (0, Settings.screen_height, Settings.screen_width, 1),
]


class Entity:
    entityDict: dict[str, Entity] = {}  # словарь всех Entity для метода Entity.fromData
    id = "entity"

    def __init__(self, screen, data: dict = None):
        from game.screen import Screen
        self.screen: Screen = screen  # экран, для доступа к списку сущностей и к клеткам мира
        self.tags: list[str] = []
        # группа к которой пренадлежит сущность, для определения нужно ли наносить урон (присваивать значение только с помощью полей класса EntityGroups)
        self.animator: Animator = None
        self.drawPriority = 1  # Чем больше, тем позже рисуется
        self.x: float = 0
        self.y: float = 0
        self.width: float = 1
        self.height: float = 1
        self.speedX: float = 0
        self.speedY: float = 0
        self.image: pygame.Surface = None
        self.imagePos: tuple[float, float] = (0, 0)
        self.hidden = False  # если True, то остальные сущности перестают проверять столкновения с этой сущностью
        self.ghostE = False  # если True, то на движение сущности не влияют другие
        self.ghostT = False  # если True, то на движение сущности не влияют клетки
        if (data):
            self.applyData(self.getDataSetter(data), data)

    @staticmethod
    def fromData(data: dict, screen: pygame.Surface) -> Entity:
        clas = data["className"]
        if (clas in Entity.entityDict):
            return Entity.entityDict[clas](screen, data)
        raise GameExeption(f"Entity.fromData: no Entity with className: {clas}")

    @staticmethod
    def createById(id: str, screen: pygame.Surface) -> Entity:
        if (id in Entity.entityDict):
            return Entity.entityDict[id](screen)
        raise GameExeption(f"Entity.fromData: no Entity with className: {id}")

    @staticmethod
    def registerEntity(id: str, entityClass):
        if (id in Entity.entityDict):
            raise GameExeption(f"Entity.registerEntity: id is already taken: {id}")
        Entity.entityDict[id] = entityClass
        entityClass.id = id

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        dataSetter("x", self.x)
        dataSetter("y", self.y)

    def getDataSetter(self, data: dict) -> Callable[[str, Any, str, Callable[[Any], Any]], None]:
        def setter(field: str, default: Any, fieldDest: str = None, fun: Callable[[Any], Any] = lambda x: x):
            if (fieldDest is None):
                fieldDest = field
            if (field in data):
                setattr(self, fieldDest, fun(data[field]))
            else:
                setattr(self, fieldDest, default)
        return setter

    def preUpdate(self):
        pass

    def update(self):
        if (self.animator is not None):
            self.animator.update()
        return self.move()

    def draw(self, surface: pygame.Surface, opaque=1):
        if (self.animator is not None):
            self.image, self.imagePos = self.animator.getImage()

        rect = multRect(self.get_rect(), Settings.tileSize)
        if (self.image is not None):
            image = self.image
            if (opaque != 1):
                image = self.image.copy()
                alpha = max(min(opaque * 255, 255), 0)
                image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
            surface.blit(image, (rect[0] + self.imagePos[0] * Settings.tileSize,
                         rect[1] + self.imagePos[1] * Settings.tileSize))

        self.draw_dev(surface)

    def draw_dev(self, surface: pygame.Surface):
        rect = multRect(self.get_rect(), Settings.tileSize)
        if (self.image is None and Settings.drawNoneImgs):
            self.draw_rect(surface, "green", rect, True)
        if (Settings.drawHitboxes):
            self.draw_rect(surface, "cyan", rect)

    def draw_rect(self, surface: pygame.Surface, color, rect, fill=False, mul=False, rel=False):
        if (mul):
            rect = multRect(rect, Settings.tileSize)
        if (rel):
            rect = (rect[0] + self.x * Settings.tileSize, rect[1] + self.y * Settings.tileSize, rect[2], rect[3])
        if (fill):
            pygame.draw.rect(surface, color, rect)
        else:
            pygame.draw.rect(surface, color, rect, round(Settings.tileSize * 0.03125) + 1)

    def move(self) -> list[tuple[tuple[float, float, float, float], Union[Tile, Entity, None]]]:
        # просчёт движения с учётом карты и сущностей. При столкновении с сущностью или клеткой возвращает эту сущность или клетку

        nX = self.x + self.speedX
        nY = self.y + self.speedY
        if (not self.ghostT):
            tile = self.get_tile(pos=(0.5, 0.95))[0]
            if (tile):
                nX = self.x + self.speedX * self.tileSpeed(tile)
                nY = self.y + self.speedY * self.tileSpeed(tile)
        newRect = (nX, nY, self.width, self.height)
        colision = []
        for (tile, x, y) in self.screen.getTiles():
            rect = (x, y, 1, 1)
            if (not rectIntersection(newRect, rect)):
                continue
            if (not self.canGoOn(tile)):
                colision.append((rect, tile))
                if (self.ghostT):
                    continue
                pos = self.move_toEdge(rect)
                r, nx, ny = self.slideAroundCorner(newRect, rect)
                if (r):
                    nX = nx
                    nY = ny
                    newRect = (nX, nY, self.width, self.height)
                    continue
                if (not rectIntersection((nX, self.y, self.width, self.height), rect)):
                    nY = self.y
                    newRect = (nX, nY, self.width, self.height)
                    continue
                if (not rectIntersection((self.x, nY, self.width, self.height), rect)):
                    nX = self.x
                    newRect = (nX, nY, self.width, self.height)
                    continue
                if (pos[0] == 0 and pos[1] == 0):
                    self.pushOutside(rect)
                return colision

        for entity in self.screen.entities:
            if (entity == self or entity.hidden):
                continue
            rect = entity.get_rect()
            if (rectIntersection(newRect, rect)):
                colision.append((rect, entity))
                if (self.ghostE or self.canPassThrough(entity)):
                    continue
                pos = self.move_toEdge(rect)
                if (not rectIntersection((nX, self.y, self.width, self.height), rect)):
                    nY = self.y
                    newRect = (nX, nY, self.width, self.height)
                    continue
                if (not rectIntersection((self.x, nY, self.width, self.height), rect)):
                    nX = self.x
                    newRect = (nX, nY, self.width, self.height)
                    continue
                if (pos[0] == 0 and pos[1] == 0):
                    self.pushOutside(rect)
                return colision

        for rect in screenBorders:
            if (not rectIntersection(newRect, rect)):
                continue
            pos = self.move_toEdge(rect)
            colision.append((rect, None))
            if (not rectIntersection((nX, self.y, self.width, self.height), rect)):
                nY = self.y
                newRect = (nX, nY, self.width, self.height)
                continue
            if (not rectIntersection((self.x, nY, self.width, self.height), rect)):
                nX = self.x
                newRect = (nX, nY, self.width, self.height)
                continue
            if (pos[0] == 0 and pos[1] == 0):
                self.pushOutside(rect)
            return colision

        self.x = nX
        self.y = nY
        return colision

    def move_toEdge(self, rect: tuple[int, int, int, int]):
        pos = self.get_relPos(rect)
        if (pos[0] < 0):
            self.x = rect[0] - self.width
        if (pos[0] > 0):
            self.x = rect[0] + rect[2]
        if (pos[1] < 0):
            self.y = rect[1] - self.height
        if (pos[1] > 0):
            self.y = rect[1] + rect[3]
        return pos

    def pushOutside(self, rect: tuple[int, int, int, int]):
        hor_c = ((self.x + self.width / 2) - (rect[0] + rect[2] / 2)) / (rect[2] / 2 + self.width / 2)
        ver_c = ((self.y + self.height / 2) - (rect[1] + rect[3] / 2)) / (rect[3] / 2 + self.height / 2)
        if (abs(hor_c) > abs(ver_c)):
            if (hor_c > 0):
                self.x = rect[0] + rect[2]
            else:
                self.x = rect[0] - self.width
        else:
            if (ver_c > 0):
                self.y = rect[1] + rect[3]
            else:
                self.y = rect[1] - self.height

    def slideAroundCorner(self, newRect: tuple[int, int, int, int], rect: tuple[int, int, int, int]):
        MaxDistance = 0.25
        def distanceToCorner(corner: tuple[int, int]):
            cornerSelf = (1 - corner[0], 1 - corner[1])
            x1 = rect[0] + rect[2] * corner[0]
            y1 = rect[1] + rect[3] * corner[1]
            x2 = newRect[0] + newRect[2] * cornerSelf[0]
            y2 = newRect[1] + newRect[3] * cornerSelf[1]
            dx = x2 - x1
            dy = y2 - y1
            distance = dx * dx + dy * dy
            return corner, (distance <= MaxDistance * MaxDistance)
        def moveToCorner(corner: tuple[int, int], confirm: bool):
            if (not confirm):
                return False, 0, 0
            if (corner[0] == 0):
                nx = rect[0] - newRect[2]
            else:
                nx = rect[0] + rect[2]
            if (corner[1] == 0):
                ny = rect[1] - newRect[3]
            else:
                ny = rect[1] + rect[3]
            return True, nx, ny
        r, nx, ny = moveToCorner(*distanceToCorner((0, 0)))
        if (r):
            return True, nx, ny
        r, nx, ny = moveToCorner(*distanceToCorner((0, 1)))
        if (r):
            return True, nx, ny
        r, nx, ny = moveToCorner(*distanceToCorner((1, 0)))
        if (r):
            return True, nx, ny
        r, nx, ny = moveToCorner(*distanceToCorner((1, 1)))
        if (r):
            return True, nx, ny
        return False, newRect[0], newRect[1]

    def get_relPos(self, rect: tuple[int, int, int, int]):
        pos = [0, 0]
        # rect = pygame.Rect(*multRect(rect, Settings.tileSize))
        # this = pygame.Rect(*multRect((self.x, self.y, self.width, self.height), Settings.tileSize))

        # if (this.x + this.width <= rect[0]):
        #     pos[0] = -1
        # if (this.x >= rect[0] + rect[2]):
        #     pos[0] = 1
        # if (this.y + this.height <= rect[1]):
        #     pos[1] = -1
        # if (this.y >= rect[1] + rect[3]):
        #     pos[1] = 1

        if (self.x + self.width <= rect[0]):
            pos[0] = -1
        if (self.x >= rect[0] + rect[2]):
            pos[0] = 1
        if (self.y + self.height <= rect[1]):
            pos[1] = -1
        if (self.y >= rect[1] + rect[3]):
            pos[1] = 1
        return pos[0], pos[1]

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)

    def canGoOn(self, tile: Tile) -> bool:
        return not tile.solid

    def canPassThrough(self, entity: Entity) -> bool:
        return False

    def tileSpeed(self, tile: Tile) -> float:
        return tile.speed

    def remove(self):
        self.screen.removeEntity(self)

    def get_tile(self, dx=0, dy=0, pos: tuple[float, float] = (0.5, 0.5)) -> Union[tuple[Tile, tuple[int, int]], tuple[None, None]]:
        x = self.x + dx + self.width * pos[0]
        y = self.y + dy + self.height * pos[1]
        x, y = int(x), int(y)
        if (x < 0 or y < 0 or x >= Settings.screen_width or y >= Settings.screen_height):
            return (None, None)
        return (self.screen.tiles[y][x], (x, y))

    def get_entities(self, rect: tuple[float, float, float, float]) -> list[Entity]:
        entities = []
        for entity in self.screen.entities:
            if (entity == self):
                continue
            if (entity.is_inRect(rect)):
                entities.append(entity)
        return entities

    def get_entitiesD(self, rect: tuple[float, float, float, float]) -> list[Entity]:
        rectSelf = self.get_rect()
        rectNew = (rectSelf[0] + rect[0], rectSelf[1] + rect[1], rect[2], rect[3])
        entities = []
        for entity in self.screen.entities:
            if (entity == self):
                continue
            if (entity.is_inRect(rectNew)):
                entities.append(entity)
        return entities

    def is_inRect(self, rect: tuple[float, float, float, float]):
        return rectIntersection(self.get_rect(), rect)

    def is_inRectD(self, rect: tuple[float, float, float, float], entity: Entity):
        rectSelf = self.get_rect()
        rectNew = (rectSelf[0] + rect[0], rectSelf[1] + rect[1], rect[2], rect[3])
        return entity.is_inRect(rectNew)

    def predictCollisions(self, x: float, y: float, w: float = None, h: float = None) -> list[tuple[tuple[float, float, float, float], Union[Tile, Entity, None]]]:
        # столкновения, если бы сущность была расположена по этим координатам
        newRect = [x, y, self.width, self.height]
        if (w):
            newRect[2] = w
        if (h):
            newRect[3] = h
        colision = []
        for (tile, x, y) in self.screen.getTiles():
            rect = (x, y, 1, 1)
            if (not rectIntersection(newRect, rect)):
                continue
            if (not self.canGoOn(tile)):
                colision.append((rect, tile))
                return colision

        for entity in self.screen.entities:
            if (entity == self or entity.hidden):
                continue
            rect = entity.get_rect()
            if (rectIntersection(newRect, rect)):
                colision.append((rect, entity))
                return colision

        for rect in screenBorders:
            if (not rectIntersection(newRect, rect)):
                continue
            colision.append((rect, None))
            return colision

        return colision


class EntityGroups:
    neutral = 0
    playerSelf = 1
    player = 2
    enemy = 3


sound_hit = load_sound("hit2.mp3", "hit")


class EntityAlive(Entity):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.group = EntityGroups.neutral
        self.health = 1
        self.healthMax = 1
        self.damageDelay = 0  # при вызове update уменьшается на 1000 / Settings.fps
        self.strength = 0
        self.alive = True
        self.immortal = False
        self.removeOnDeath = True
        self.damageAnimCounter = 0
        self.DamageDelay = Settings.damageDelay
        self.attackPushback = True
        self.attackPushbackX = 0
        self.attackPushbackY = 0
        self.attackPushbackA = 0.002

    def takeDamage(self, damage: int, attacker: Union[Entity, str, None] = None):
        if (self.immortal or damage == 0):
            return False
        if (self.alive and self.animator):
            self.animator.startDamageAnim()
        if (self.damageDelay > 0):
            return False
        sound_hit.play()
        self.damageDelay = self.DamageDelay
        self.health -= damage
        if (isinstance(attacker, Entity) and self.attackPushback):
            dx = (attacker.x + attacker.width / 2) - (self.x + self.width / 2)
            dy = (attacker.y + attacker.height / 2) - (self.y + self.height / 2)
            self.attackPushbackX = -0.1 * (dx / (self.width + attacker.width))
            self.attackPushbackY = -0.1 * (dy / (self.height + attacker.height))
        if (self.health <= 0):
            self.alive = False
            self.hidden = True
            self.speedX = 0
            self.speedY = 0
            if (self.animator and "stay" in self.animator.data.frames):
                self.animator.setAnimation("stay")
        return True

    def heal(self, v: int):
        self.health += v
        self.health = min(self.health, self.healthMax)

    def onDeath(self):
        pass

    def update(self):
        self.attackPushbackX = max((abs(self.attackPushbackX) - self.attackPushbackA), 0) * \
            (1 if self.attackPushbackX >= 0 else -1)
        self.attackPushbackY = max((abs(self.attackPushbackY) - self.attackPushbackA), 0) * \
            (1 if self.attackPushbackY >= 0 else -1)
        speedX = self.speedX
        speedY = self.speedY
        self.speedX += self.attackPushbackX
        self.speedY += self.attackPushbackY
        collisions = super().update()
        self.speedX = speedX
        self.speedY = speedY
        if (not self.alive):
            if (self.removeOnDeath):
                if (self.animator):
                    if (self.animator.damageAnimFinished or not self.animator.damageAnim):
                        self.onDeath()
                        self.remove()
                else:
                    self.onDeath()
                    self.remove()
            return collisions
        if (self.damageDelay > 0):
            self.damageDelay -= 1000 / Settings.fps
        for rect, collision in collisions:
            if (isinstance(collision, Tile)):
                self.takeDamage(collision.damage(rect[0], rect[1]), collision.id)
                continue
            if (not isinstance(collision, EntityAlive) or not collision.alive):
                continue
            if (self.group == EntityGroups.playerSelf):
                if (collision.group == EntityGroups.enemy or
                        collision.group == EntityGroups.neutral):
                    collision.takeDamage(self.strength, self)
                    self.takeDamage(collision.strength, collision)
            elif (self.group == EntityGroups.player):
                if (collision.group == EntityGroups.enemy or
                        collision.group == EntityGroups.neutral):
                    collision.takeDamage(self.strength, self)
                    self.takeDamage(collision.strength, collision)
            elif (self.group == EntityGroups.enemy):
                if (collision.group == EntityGroups.player or
                        collision.group == EntityGroups.playerSelf):
                    collision.takeDamage(self.strength, self)
                    self.takeDamage(collision.strength, collision)
                if (collision.group == EntityGroups.neutral):
                    self.takeDamage(collision.strength, collision)
            elif (self.group == EntityGroups.neutral):
                if (collision.group == EntityGroups.player or
                        collision.group == EntityGroups.playerSelf):
                    collision.takeDamage(self.strength, self)
                    self.takeDamage(collision.strength, collision)
                if (collision.group == EntityGroups.enemy):
                    collision.takeDamage(self.strength, self)

        tileUnder, pos = self.get_tile(pos=(0.5, 1))
        if (tileUnder):
            damage = tileUnder.damage(*pos)
            if (damage != 0):
                self.takeDamage(damage, tileUnder.id)
        return collisions


def loadEntities():
    import game.entities.entities
    import game.entities.shovel
    import game.entities.crab
    import game.entities.coin
    import game.entities.pirate2
    import game.entities.heart
    import game.entities.market
    import game.entities.trader
    import game.entities.trainer
    import game.entities.cannon
    import game.entities.trigger
    import game.entities.cactusDancing
    import game.entities.cactusDancingChild
    import game.entities.aborigine
    import game.entities.aborigineBow
    import game.entities.skeleton
    import game.entities.skeletonShield
    import game.entities.tentacle
    import game.entities.piranha
    import game.entities.lavaBubble
    import game.entities.spear
    import game.entities.octopus
    import game.entities.stone
    import game.entities.pirate3


loadEntities()
