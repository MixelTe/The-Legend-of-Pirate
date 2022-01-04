from game.entity import Entity, EntityAlive

class EntityCrab(EntityAlive):
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.width = 0.8
        self.height = 0.677
