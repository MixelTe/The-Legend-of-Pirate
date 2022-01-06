from game.entity import EntityAlive

class EntityCrab(EntityAlive):
    def __init__(self, screen, data: dict=None):
        super().__init__(screen, data)
        self.width = 0.8
        self.height = 0.677
        self.imgRect = [0, 0, 0.8, 0.677]
        self.speed = 0.04
        self.speedX = self.speed
        self.speedY = self.speed

    def update(self):
        rect, collision = super().update()
        if (collision is None or rect is None):
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
