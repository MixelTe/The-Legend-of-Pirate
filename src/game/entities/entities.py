import pygame
from functions import load_entity
from game.entity import Entity, EntityAlive, EntityGroups
from settings import Settings


class EntityCactus(EntityAlive):
    image = pygame.transform.scale(load_entity("cactus.png"), (Settings.tileSize * 1, Settings.tileSize * 1))
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.image = EntityCactus.image
        self.width = 1
        self.height = 1
        self.group = EntityGroups.neutral


class EntityDoor(Entity):
    image = pygame.transform.scale(load_entity("door.png"), (Settings.tileSize * 1, Settings.tileSize * 1))
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.image = EntityDoor.image
        self.width = 1
        self.height = 1


class EntityPalm(Entity):
    image = pygame.transform.scale(load_entity("palm.png"), (Settings.tileSize * 1.5, Settings.tileSize * 1.5))
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.image = EntityPalm.image
        self.width = 0.45
        self.height = 0.7
        self.imagePos = (-0.45, -0.8)


class EntityTrader(Entity):
    image = pygame.transform.scale(load_entity("stay.png", "trader").subsurface(0, 0, 14, 24), (Settings.tileSize * 0.75, Settings.tileSize * 1.5))
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.image = EntityTrader.image
        self.width = 0.75
        self.height = 1
        self.imagePos = (0, -0.5)


class EntityCannon(Entity):
    image = pygame.transform.scale(load_entity("stay.png", "cannon").subsurface(0, 0, 11, 12), (Settings.tileSize * 1, Settings.tileSize * 1))
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.image = EntityCannon.image
        self.width = 1
        self.height = 1


class EntityTrainer(EntityAlive):
    image = pygame.transform.scale(load_entity("trainer.png"), (Settings.tileSize * 0.75, Settings.tileSize * 1.5))
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.image = EntityTrainer.image
        self.width = 0.75
        self.height = 1
        self.imagePos = (0, -0.5)
        self.group = EntityGroups.enemy

