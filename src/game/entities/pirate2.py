import pygame
from game.animator import Animator, AnimatorData
from game.entity import Entity
from settings import Settings


animatorData = AnimatorData("pirate2", [
    ("stay.png", 500, (11, 22), (0, -0.8, 0.75, 1.5)),
])


class EntityPirate2(Entity):
    def __init__(self, screen, data: dict = None):
        self.speech = ""
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.width = 0.75
        self.height = 0.7
        self.talkZone = (-1, -1, 2, 2)

    def applyData(self, data: dict):
        super().applyData(data)
        if ("speech" in data):
            self.speech = data["speech"]

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        if (Settings.drawHitboxes):
            self.draw_rect(surface, "pink", self.talkZone, False, True, True)

    def update(self):
        super().update()
        if (self.is_inRectD(self.talkZone, self.screen.player)):
            self.screen.player.message = self.speech


Entity.registerEntity("pirate2", EntityPirate2)
