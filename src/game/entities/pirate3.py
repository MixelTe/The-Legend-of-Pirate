from typing import Any, Callable
import pygame
from game.animator import Animator, AnimatorData
from game.entity import Entity
from settings import Settings


animatorData = AnimatorData("pirate3", [
    ("stay.png", 500, (11, 22), (0, -0.8, 0.75, 1.5)),
    ("stay1.png", 500, (11, 22), (0, -0.8, 0.75, 1.5)),
    ("stay2.png", 500, (11, 22), (0, -0.8, 0.75, 1.5)),
])


class EntityPirate3(Entity):
    def __init__(self, screen, data: dict = None):
        self.speech = ""
        self.img = 1
        super().__init__(screen, data)
        self.animator = Animator(animatorData, f"stay{self.img}")
        self.width = 0.75
        self.height = 0.7
        self.talkZone = (-1, -1, 3, 3)

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        super().applyData(dataSetter, data)
        dataSetter("speech", self.speech)
        dataSetter("img", self.img)
        self.img = min(2, max(1, int(self.img)))

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        if (Settings.drawHitboxes):
            self.draw_rect(surface, "pink", self.talkZone, False, True, True)

    def update(self):
        super().update()
        if (self.is_inRectD(self.talkZone, self.screen.player)):
            self.screen.player.message = self.speech


Entity.registerEntity("pirate3", EntityPirate3)
