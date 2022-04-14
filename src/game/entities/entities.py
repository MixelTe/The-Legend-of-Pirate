import math
from typing import Any, Callable
import pygame
from functions import load_entityImg, load_image, load_sound, multRect, removeFromCollisions, scaleImg
from game.entity import Entity, EntityAlive, EntityGroups
from game.animator import Animator, AnimatorData
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
        self.content = "random"
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

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        dataSetter("content", self.content)

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
        self.tags.append("low")
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


class EntityStoneBar(Entity):
    image = load_entityImg("stoneBar.png", 1, 1)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityStoneBar.image

    def update(self):
        pass


Entity.registerEntity("stoneBar", EntityStoneBar)


class EntityBone(EntityAlive):
    image = load_entityImg("bone.png", 0.8, 0.42)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityBone.image
        self.group = EntityGroups.enemy
        self.strength = 1
        self.speed = 0.08
        self.width = 0.8
        self.height = 0.8
        self.rotation = 0

    def canGoOn(self, tile: Tile) -> bool:
        return super().canGoOn(tile) or "low" in tile.tags

    def canPassThrough(self, entity: Entity) -> bool:
        return "low" in entity.tags

    def draw(self, surface: pygame.Surface):
        self.image = pygame.transform.rotate(EntityBone.image, self.rotation)
        v = 0.4
        if (self.rotation < 90):
            self.imagePos = (-math.cos(self.rotation / 180 * math.pi) * v + v,
                             -math.sin(self.rotation / 180 * math.pi) * v + v)
        elif (self.rotation < 180):
            self.imagePos = (math.cos(self.rotation / 180 * math.pi) * v + v,
                             -math.sin(self.rotation / 180 * math.pi) * v + v)
        elif (self.rotation < 270):
            self.imagePos = (math.cos(self.rotation / 180 * math.pi) * v + v,
                             math.sin(self.rotation / 180 * math.pi) * v + v)
        elif (self.rotation < 360):
            self.imagePos = (-math.cos(self.rotation / 180 * math.pi) * v + v,
                             math.sin(self.rotation / 180 * math.pi) * v + v)
        super().draw(surface)

    def update(self):
        collisions = super().update()
        self.rotation = (self.rotation + (1000 / Settings.fps) / 2) % 360
        removeFromCollisions(collisions, [], ["low"])
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

    def canPassThrough(self, entity: Entity) -> bool:
        return "low" in entity.tags

    def update(self):
        collisions = super().update()
        removeFromCollisions(collisions, ["tentacle"], ["low"])
        if (len(collisions) != 0):
            self.remove()


Entity.registerEntity("ink", EntityInk)


class EntityWood(Entity):
    image = load_entityImg("wood.png", 0.875, 0.4375)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.tags.append("low")
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
        self.tags.append("low")
        self.image = EntityWood2.image
        self.width = 0.6875
        self.height = 0.625
        self.imagePos = (-0.125, 0)

    def update(self):
        pass


Entity.registerEntity("wood2", EntityWood2)


class EntityArrow(EntityAlive):
    image = load_entityImg("arrow.png", 0.75, 0.25)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityArrow.image
        self.group = EntityGroups.enemy
        self.ghostT = True
        self.ghostE = True
        self.strength = 1
        self.speed = 0.1
        self.width = 0.75
        self.height = 0.25

    def canGoOn(self, tile: Tile) -> bool:
        return super().canGoOn(tile) or "low" in tile.tags

    def canPassThrough(self, entity: Entity) -> bool:
        return "low" in entity.tags

    def draw(self, surface: pygame.Surface, opaque=1):
        rotation = math.atan2(-self.speedY, self.speedX) / math.pi * 180
        self.image = pygame.transform.rotate(EntityArrow.image, rotation)
        super().draw(surface, opaque)

    def update(self):
        collisions = super().update()
        removeFromCollisions(collisions, ["aborigineBow"], ["low"])
        if (len(collisions) != 0):
            self.remove()


Entity.registerEntity("arrow", EntityArrow)


class EntityLavaPath(EntityAlive):
    animatorData = AnimatorData("lavaPath", [
        ("stay.png", 600, (16, 16), (0, 0, 1, 1)),
    ])

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.tags.append("low")
        self.animator = Animator(EntityLavaPath.animatorData, "stay")
        self.group = EntityGroups.enemy
        self.hidden = True
        self.ghostT = True
        self.ghostE = True
        self.drawPriority = 0
        self.strength = 1
        self.width = 1
        self.height = 1
        self.imagePos = (0, 0)
        self.counter = 1

    def draw(self, surface: pygame.Surface, opaque=1):
        self.image, _ = self.animator.getImage()

        rect = multRect(self.get_rect(), Settings.tileSize)
        if (self.image is not None):
            image = self.image
            surface.blit(image, (rect[0] + self.imagePos[0] * Settings.tileSize,
                         rect[1] + self.imagePos[1] * Settings.tileSize))

        self.draw_dev(surface)

    def update(self):
        super().update()
        if (self.animator.lastState[1]):
            self.remove()
        if (self.animator.lastState[0]):
            v = 0.1
            self.width -= v
            self.height -= v
            self.x += v / 2
            self.y += v / 2
            self.imagePos = (self.imagePos[0] - v / 2, self.imagePos[1] - v / 2)


Entity.registerEntity("lavaPath", EntityLavaPath)


class EntitySpyglass(Entity):
    image = load_entityImg("spyglass.png", 0.6875, 0.25)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.tags.append("low")
        self.image = EntitySpyglass.image
        self.width = 0.6875
        self.height = 0.25
        self.hidden = True
        self.ghostE = True

    def update(self):
        if ("quest-pirate-tubeFound" in self.screen.saveData.tags):
            self.remove()
        if (self.screen.player.is_inRect(self.get_rect())):
            self.screen.player.takeItem(self)
            self.remove()
            self.screen.saveData.tags.append("quest-pirate-tubeFound")


Entity.registerEntity("spyglass", EntitySpyglass)


class EntityMap(Entity):
    image1 = scaleImg(load_image("map1.png"), 1.03, 0.56)
    image2 = scaleImg(load_image("map2.png"), 1.03, 0.56)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.tags.append("low")
        self.image = EntityMap.image1
        self.width = 1.03
        self.height = 0.56

    def setImg(self, img: int):
        if (img == 1):
            self.image = EntityMap.image1
        else:
            self.image = EntityMap.image2

    def update(self):
        pass


Entity.registerEntity("map", EntityMap)


class EntityHeartAdd(Entity):
    image = scaleImg(load_image("hpA.png"), 0.7, 0.7)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityHeartAdd.image
        self.hidden = True
        self.ghostE = True
        self.width = 0.7
        self.height = 0.7

    def update(self):
        pass


Entity.registerEntity("heart_add", EntityHeartAdd)


class EntityDigPlaceHidden(Entity):
    def __init__(self, screen, data: dict = None):
        self.content = "heart_add"
        super().__init__(screen, data)
        self.hidden = True
        self.ghostE = True
        self.ghostT = True
        self.width = 1
        self.height = 1

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        dataSetter("content", self.content)

    def dig(self):
        if (self.content == "heart_add"):
            if ("heart-collected" in self.screen.player.saveData.tags):
                return
            if ("quest-pirate-ended" not in self.screen.player.saveData.tags or
                "quest-cactus-ended" not in self.screen.player.saveData.tags):
                return
            heart = Entity.createById("heart_add", self.screen)
            self.screen.player.takeItem(heart)
            self.screen.player.saveData.tags.append("heart-collected")
            self.screen.player.healthMax = 8
            self.screen.player.health = 8


Entity.registerEntity("dig_place_hidden", EntityDigPlaceHidden)


class EntityСoinbag(Entity):
    image = scaleImg(load_image("coinbag.png"), 0.9375, 0.75)

    def __init__(self, screen, data: dict = None):
        self.bagId = 1
        super().__init__(screen, data)
        self.tags.append("low")
        self.image = EntityСoinbag.image
        self.width = 0.9375
        self.height = 0.75
        self.hidden = True
        self.ghostE = True

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        dataSetter("id", self.bagId, "bagId")

    def update(self):
        if (f"coinbag-{self.bagId}" in self.screen.saveData.tags):
            self.remove()
        if (self.screen.player.is_inRect(self.get_rect())):
            self.screen.player.takeItem(self)
            self.remove()
            self.screen.saveData.tags.append(f"coinbag-{self.bagId}")


Entity.registerEntity("coinbag", EntityСoinbag)
