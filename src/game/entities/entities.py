from functions import load_entityImg, load_entityStay
from game.entity import Entity, EntityAlive, EntityGroups


class EntityCactus(EntityAlive):
    image = load_entityImg("cactus.png", 1, 1)
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.image = EntityCactus.image
        self.width = 1
        self.height = 1
        self.strength = 1
        self.group = EntityGroups.neutral


class EntityDoor(Entity):
    image = load_entityImg("door.png", 1, 1)
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.image = EntityDoor.image
        self.width = 1
        self.height = 1


class EntityPalm(Entity):
    image = load_entityImg("palm.png", 1.5, 1.5)
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.image = EntityPalm.image
        self.width = 0.45
        self.height = 0.7
        self.imagePos = (-0.45, -0.8)


class EntityTrader(Entity):
    image = load_entityStay("trader", 14, 24, 0.75, 1.5)
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.image = EntityTrader.image
        self.width = 0.75
        self.height = 1
        self.imagePos = (0, -0.5)


class EntityCannon(Entity):
    image = load_entityStay("cannon", 11, 12, 1, 1)
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.image = EntityCannon.image
        self.width = 1
        self.height = 1


class EntityTrainer(EntityAlive):
    image = load_entityImg("trainer.png", 0.75, 1.5)
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.image = EntityTrainer.image
        self.width = 0.75
        self.height = 1
        self.imagePos = (0, -0.5)
        self.group = EntityGroups.enemy

