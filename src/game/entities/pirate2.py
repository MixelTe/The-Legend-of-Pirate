import pygame
from game.animator import Animator, AnimatorData
from game.entity import Entity
from settings import Settings


animatorData = AnimatorData("pirate2", [
    ("stay.png", 500, (11, 22), (0, -0.8, 0.75, 1.5)),
])


class EntityPirate2(Entity):
    def __init__(self, screen, data: dict = None):
        self.speech = "Эй, Капитан! Тут какая-то странная дверь, за ней, должно быть, наш корабль или то, что от него осталось, хехе!"
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.width = 0.75
        self.height = 0.7
        self.talkZone = (-1, -1, 2, 2)

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        if (Settings.drawHitboxes):
            self.draw_rect(surface, "pink", self.talkZone, False, True, True)

    def update(self):
        super().update()
        if (self.is_inRectD(self.talkZone, self.screen.player)):
            if ("island-door" in self.screen.saveData.tags):
                self.screen.player.message = "Ничего себе! А ключом было никак?"
            else:
                self.screen.player.message = self.speech

Entity.registerEntity("pirate2", EntityPirate2)
