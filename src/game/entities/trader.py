import pygame
from game.entity import Entity
from game.animator import AnimatorData, Animator
from settings import Settings

animatorData = AnimatorData("trader", [
    ("stay.png", 0, (14, 24), (0, -0.8, 0.75, 1.5)),
    ("trade.png", 2500, (14, 24), (0, -0.8, 0.75, 1.5)),
])


class EntityTrader(Entity):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.width = 0.75
        self.height = 0.7
        self.imagePos = (0, -0.8)
        self.talkZone = (-1, 0, 3, 3)
        self.speeches = ["Извини капитан, теперь каждый сам за себя!"]
        self.speech = self.speeches[0]

    def somethingBought(self, speech):
        self.animator.setAnimation("trade")
        self.speech = speech

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        if (Settings.drawHitboxes):
            self.draw_rect(surface, "pink", self.talkZone, False, True, True)

    def setSpeech(self, speech):
        if (self.animator.anim != "trade"):
            self.speech = speech

    def preUpdate(self):
        if (self.animator.anim != "trade"):
            self.speech = self.speeches[0]

    def update(self):
        super().update()
        if (self.is_inRectD(self.talkZone, self.screen.player)):
            self.screen.player.message = self.speech
        if (self.animator.anim == "trade"):
            if (self.animator.lastState[1]):
                self.animator.setAnimation("stay")
                self.speech = self.speeches[0]


Entity.registerEntity("trader", EntityTrader)
