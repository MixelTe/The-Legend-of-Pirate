from functions import dropCoin
from game.animator import Animator, AnimatorData
from game.entity import EntityAlive, EntityGroups
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("skeletonShield", [
    ("stay.png", 0, (9, 13), (0, 0, 0.69, 1)),
])


class EntitySkeletonShield(EntityAlive):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.group = EntityGroups.enemy
        self.strength = 1
        self.healthMax = 2
        self.health = 2
        self.width = 0.69
        self.height = 1

    def canGoOn(self, tile: Tile) -> bool:
        return "water" not in tile.tags and super().canGoOn(tile)

    def onDeath(self):
        dropCoin(self)

    def update(self):
        super().update()
        if (not self.alive or Settings.disableAI):
            return


EntityAlive.registerEntity("skeletonShield", EntitySkeletonShield)
