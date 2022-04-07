import math
import pygame
from functions import load_entityImg, load_sound, removeFromCollisions
from game.entity import Entity, EntityAlive, EntityGroups
from random import random
from game.tile import Tile

from settings import Settings


class EntityCactus(EntityAlive):
    image = load_entityImg("cactus.png", 1, 1)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityCactus.image
        self.immortal = True
        self.width = 0.85
        self.height = 0.85
        self.strength = 1
        self.imagePos = (-0.075, -0.075)
        self.group = EntityGroups.neutral
        self.damageAura = (-0.075, -0.075, 1, 1)

    def update(self):
        super().update()
        for e in self.get_entitiesD(self.damageAura):
            if (isinstance(e, EntityAlive)):
                e.takeDamage(self.strength, self)


Entity.registerEntity("cactus", EntityCactus)


class EntityDoor(Entity):
    image = load_entityImg("door.png", 1, 1)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityDoor.image
        self.width = 1
        self.height = 1

    def update(self):
        if ("island-door" in self.screen.saveData.tags):
            self.remove()


Entity.registerEntity("door", EntityDoor)


class EntityPalm(Entity):
    image = load_entityImg("palm.png", 1.5, 1.5)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityPalm.image
        self.width = 0.45
        self.height = 0.7
        self.imagePos = (-0.45, -0.8)

    def update(self):
        pass

Entity.registerEntity("palm", EntityPalm)


class EntityCannonball(EntityAlive):
    image = load_entityImg("cannonball.png", 0.4, 0.4)
    sound_boom = load_sound("doorBoom.wav")

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityCannonball.image
        self.group = EntityGroups.enemy
        self.strength = 100
        self.hidden = True
        self.ghostE = True
        self.width = 0.4
        self.height = 0.4

    def update(self):
        collisions = super().update()
        for rect, collision in collisions:
            if (isinstance(collision, EntityDoor)):
                self.screen.saveData.tags.append("island-door")
                self.remove()
                collision.remove()
                EntityCannonball.sound_boom.play()


Entity.registerEntity("cannonball", EntityCannonball)


class EntityDigPlace(Entity):
    image = load_entityImg("dig_place.png", 0.3, 0.3)
    image2 = load_entityImg("dig_place2.png", 1, 1)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityDigPlace.image
        self.hidden = True
        self.ghostE = True
        self.ghostT = True
        self.drawPriority = 0
        self.width = 1
        self.height = 1
        self.imagePos = (random() * 0.5 + 0.2, random() * 0.5 + 0.2)
        self.digged = False

    def dig(self):
        self.image = EntityDigPlace.image2
        self.imagePos = (self.imagePos[0] - 0.35, self.imagePos[1] - 0.35)
        self.digged = True


Entity.registerEntity("dig_place", EntityDigPlace)


class EntityBush(Entity):
    image = load_entityImg("bush.png", 1, 1)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityBush.image
        self.hidden = True
        self.ghostE = True
        self.active = False

    def update(self):
        self.active = self.screen.player.is_inRect(self.get_rect())

    def draw(self, surface: pygame.Surface, opaque=1):
        if (self.active):
            return super().draw(surface, 0.7)
        return super().draw(surface, opaque)


Entity.registerEntity("bush", EntityBush)


class EntityStone(Entity):
    image = load_entityImg("stone.png", 1, 1)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityStone.image

    def update(self):
        pass


Entity.registerEntity("stone", EntityStone)


class EntityStoneBar(Entity):
    image = load_entityImg("stoneBar.png", 1, 1)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityStoneBar.image

    def update(self):
        pass


Entity.registerEntity("stoneBar", EntityStoneBar)


class EntityBone(EntityAlive):
    image = load_entityImg("bone.png", 0.6, 0.315)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityBone.image
        self.group = EntityGroups.enemy
        self.strength = 1
        self.speed = 0.08
        self.width = 0.6
        self.height = 0.6
        self.rotation = 0

    def canGoOn(self, tile: Tile) -> bool:
        return super().canGoOn(tile) or "low" in tile.tags

    def draw(self, surface: pygame.Surface):
        self.image = pygame.transform.rotate(EntityBone.image, self.rotation)
        if (self.rotation < 90):
            self.imagePos = (-math.cos(self.rotation / 180 * math.pi) * 0.3 + 0.3,
                             -math.sin(self.rotation / 180 * math.pi) * 0.3 + 0.3)
        elif (self.rotation < 180):
            self.imagePos = (math.cos(self.rotation / 180 * math.pi) * 0.3 + 0.3,
                             -math.sin(self.rotation / 180 * math.pi) * 0.3 + 0.3)
        elif (self.rotation < 270):
            self.imagePos = (math.cos(self.rotation / 180 * math.pi) * 0.3 + 0.3,
                             math.sin(self.rotation / 180 * math.pi) * 0.3 + 0.3)
        elif (self.rotation < 360):
            self.imagePos = (-math.cos(self.rotation / 180 * math.pi) * 0.3 + 0.3,
                             math.sin(self.rotation / 180 * math.pi) * 0.3 + 0.3)
        super().draw(surface)

    def update(self):
        collisions = super().update()
        self.rotation = (self.rotation + (1000 / Settings.fps) / 2) % 360
        if (len(collisions) != 0):
            self.remove()


Entity.registerEntity("bone", EntityBone)


class EntityInk(EntityAlive):
    image = load_entityImg("ink.png", 0.6, 0.6)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityInk.image
        self.group = EntityGroups.enemy
        self.ghostT = True
        self.ghostE = True
        self.strength = 1
        self.speed = 0.1
        self.width = 0.6
        self.height = 0.6

    def canGoOn(self, tile: Tile) -> bool:
        return super().canGoOn(tile) or "low" in tile.tags

    def update(self):
        collisions = super().update()
        removeFromCollisions(collisions, ["tentacle"])
        if (len(collisions) != 0):
            self.remove()


Entity.registerEntity("ink", EntityInk)


class EntityWood(Entity):
    image = load_entityImg("wood.png", 0.875, 0.4375)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityWood.image
        self.width = 0.875
        self.height = 0.25
        self.imagePos = (0, -0.1875)

    def update(self):
        pass

Entity.registerEntity("wood", EntityWood)


class EntityWood2(Entity):
    image = load_entityImg("wood2.png", 0.9375, 0.625)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityWood2.image
        self.width = 0.6875
        self.height = 0.625
        self.imagePos = (-0.125, 0)

    def update(self):
        pass

Entity.registerEntity("wood2", EntityWood2)


class EntityArrow(EntityAlive):
    image = load_entityImg("arrow.png", 0.6, 0.2)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityArrow.image
        self.group = EntityGroups.enemy
        self.ghostT = True
        self.ghostE = True
        self.strength = 1
        self.speed = 0.1
        self.width = 0.6
        self.height = 0.2

    def canGoOn(self, tile: Tile) -> bool:
        return super().canGoOn(tile) or "low" in tile.tags

    def draw(self, surface: pygame.Surface, opaque=1):
        rotation = math.atan2(-self.speedY, self.speedX) / math.pi * 180
        self.image = pygame.transform.rotate(EntityArrow.image, rotation)
        super().draw(surface, opaque)

    def update(self):
        collisions = super().update()
        removeFromCollisions(collisions, ["aborigineBow"])
        if (len(collisions) != 0):
            self.remove()


Entity.registerEntity("arrow", EntityArrow)