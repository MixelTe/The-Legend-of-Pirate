from game.animator import Animator, AnimatorData
from game.entity import EntityAlive, EntityGroups
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("skeleton", [
    ("stay.png", 0, (9, 13), (0, 0, 0.69, 1)),
])


class EntitySkeleton(EntityAlive):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.group = EntityGroups.enemy
        self.strength = 1
        self.healthMax = 2
        self.health = 2
        self.width = 1
        self.height = 1.06

    def canGoOn(self, tile: Tile) -> bool:
        return "water" not in tile.tags

    def onDeath(self):
        coin = EntityAlive.createById("coin", self.screen)
        self.screen.addEntity(coin)
        coin.x = self.x + self.width / 2
        coin.y = self.y + self.height / 2

    def update(self):
        super().update()
        if (not self.alive or Settings.disableAI):
            return


EntityAlive.registerEntity("skeleton", EntitySkeleton)
