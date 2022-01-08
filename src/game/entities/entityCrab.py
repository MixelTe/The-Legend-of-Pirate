import pygame
from functions import load_entity
from game.entity import EntityAlive, EntityGroups
from settings import Settings


image = load_entity("crab.png")
image = image.subsurface(0, 0, 20, 11)
image = pygame.transform.scale(image, (Settings.tileSize * 1, Settings.tileSize * 0.55))


class EntityCrab(EntityAlive):
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.group = EntityGroups.enemy
        self.width = 1
        self.height = 0.55
        self.speed = 0.04
        self.speedX = self.speed
        self.speedY = self.speed
        self.image = image

    def update(self):
        collisions = super().update()
        for rect, collision in collisions:
            if (rect is None):
                return

            pos = self.get_relPos(rect)
            if (pos[0] > 0):
                self.speedX = self.speed
            if (pos[0] < 0):
                self.speedX = -self.speed
            if (pos[1] > 0):
                self.speedY = self.speed
            if (pos[1] < 0):
                self.speedY = -self.speed
