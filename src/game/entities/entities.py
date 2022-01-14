from functions import load_entityImg, load_entityStay
from game.entity import Entity, EntityAlive, EntityGroups
from random import random


class EntityCactus(EntityAlive):
    image = load_entityImg("cactus.png", 1, 1)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityCactus.image
        self.width = 0.85
        self.height = 0.85
        self.strength = 1
        self.imagePos = (-0.075, -0.075)
        self.group = EntityGroups.neutral


Entity.registerEntity("cactus", EntityCactus)


class EntityDoor(Entity):
    image = load_entityImg("door.png", 1, 1)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityDoor.image
        self.width = 1
        self.height = 1


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


class EntityCannon(Entity):
    image = load_entityStay("cannon", 11, 12, 1, 1)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityCannon.image
        self.width = 1
        self.height = 1


Entity.registerEntity("cannon", EntityCannon)


class EntityTrainer(EntityAlive):
    image = load_entityImg("trainer.png", 0.75, 1.5)

    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.image = EntityTrainer.image
        self.immortal = True
        self.width = 0.75
        self.height = 0.7
        self.imagePos = (0, -0.8)
        self.group = EntityGroups.enemy


Entity.registerEntity("trainer", EntityTrainer)


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
