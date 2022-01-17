from functions import load_entityImg
from game.entity import Entity, EntityAlive, EntityGroups
from random import random


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
        return super().update()


Entity.registerEntity("door", EntityDoor)


class EntityPalm(Entity):
    image = load_entityImg("palm.png", 1.5, 1.5)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityPalm.image
        self.width = 0.45
        self.height = 0.7
        self.imagePos = (-0.45, -0.8)


Entity.registerEntity("palm", EntityPalm)


class EntityCannonball(EntityAlive):
    image = load_entityImg("cannonball.png", 0.4, 0.4)

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
        collisions =  super().update()
        for rect, collision in collisions:
            if (isinstance(collision, EntityDoor)):
                self.screen.saveData.tags.append("island-door")
                self.remove()
                collision.remove()



Entity.registerEntity("cannonball", EntityCannonball)


class EntityDigPlace(Entity):
    image = load_entityImg("dig_place.png", 0.3, 0.3)

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


Entity.registerEntity("dig_place", EntityDigPlace)
