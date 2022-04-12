import pygame
from game.animator import Animator, AnimatorData
from game.entity import Entity
from settings import Settings


animatorData = AnimatorData("pirate2", [
    ("stay.png", 500, (11, 22), (0, -0.8, 0.75, 1.5)),
])
TEXTS = {
    0: "Эй, ты тоже на этом острове застрял? Тут по всюду какие-то чудаки, вот я от них и спрятался, а ты я смотрю смелый.",
    1: "Кстати, они утащили мою счастливую подзорную трубу, не поможешь?",
    2: "Какие-то чудаки утащили мою счастливую подзорную трубу, не поможешь?",
    3: "Ого, спасибо огромное. Теперь, когда Ненси со мной, мы точно не пропадём! Держи в благодарность.",
    4: "Cпасибо за помощь. Теперь, когда Ненси со мной, мы точно не пропадём!",
}


class EntityPirate2(Entity):
    def __init__(self, screen, data: dict = None):
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "stay")
        self.width = 0.75
        self.height = 0.7
        self.talkZone = (-1, -1, 3, 3)
        self.speech = 0
        self.speeches = [0]
        self.giveMap = False
        if ("quest-pirate-ended" in self.screen.saveData.tags):
            self.speeches = [4]
        elif ("quest-pirate-tubeFound" not in self.screen.saveData.tags and
                "quest-pirate-started" not in self.screen.saveData.tags):
            self.speeches = [0, 1]
            self.screen.saveData.tags.append("quest-pirate-started")
        elif ("quest-pirate-tubeFound" not in self.screen.saveData.tags and
                "quest-pirate-started" in self.screen.saveData.tags):
            self.speeches = [2]
        elif ("quest-pirate-tubeFound" in self.screen.saveData.tags and
                "quest-pirate-started" not in self.screen.saveData.tags):
            self.speeches = [0, 1, 3]
            self.screen.saveData.tags.append("quest-pirate-started")
            self.screen.saveData.tags.append("quest-pirate-ended")
            self.giveMap = True
        else:
            self.speeches = [3]
            self.screen.saveData.tags.append("quest-pirate-ended")
            self.giveMap = True

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        if (Settings.drawHitboxes):
            self.draw_rect(surface, "pink", self.talkZone, False, True, True)

    def update(self):
        super().update()
        if (self.is_inRectD(self.talkZone, self.screen.player)):
            self.screen.player.action = self.nextSpeach
            self.screen.player.message = TEXTS[self.speeches[self.speech]]
            if (len(self.speeches) > 1):
                self.screen.player.messageIsLong = True
            if (self.giveMap):
                self.giveMap = False
                Map = Entity.createById("map", self.screen)
                Map.setImg(2 if "quest-cactus-ended" in self.screen.saveData.tags else 1)
                self.screen.player.takeItem(Map)

    def nextSpeach(self):
        self.speech = (self.speech + 1) % len(self.speeches)

Entity.registerEntity("pirate2", EntityPirate2)
