from typing import Any, Callable, Union
from backMusic import getCurMusic, startMusicBreak
from functions import joinPath
from game.entity import Entity, EntityAlive, EntityGroups
from game.animator import Animator, AnimatorData
from settings import Settings


animations = [
    ("stay.png", 0, (18, 24), (-0.3, -0.9, 1.125, 1.5)),
    ("dancing.png", 200, (20, 24), (-0.3625, -0.9, 1.25, 1.5)),
]


def addAnim(id: str):
    animations.append((f"appear{id}.png", 200, (18, 24), (-0.3, -0.9, 1.125, 1.5)))
    animations.append((f"cactus{id}.png", 0, (16, 16), (-0.075, -0.075, 1, 1)))


for i in range(1, 5):
    addAnim(i)

animatorData = AnimatorData("cactusDancingChild", animations)
musicPath = joinPath(Settings.folder_data, Settings.folder_sounds, "back", "background2.mp3")
TEXTS = {
    0: "Спасибо за игру!",
    1: "Хехе, у тебя полулось",
    2: "Серьёзно, так быстро?",
    3: "Не думал, что такой внимательный",
    4: "Уги-вуги!",
    5: "А меня ты уже находил!)"
}


class EntityCactusDancingChild(EntityAlive):
    def __init__(self, screen, data: dict = None):
        self.X = 0
        self.Y = 0
        self.color = 1
        super().__init__(screen, data)
        self.animator = Animator(animatorData, f"cactus{self.color}")
        self.immortal = True
        self.width = 0.85
        self.height = 0.85
        self.group = EntityGroups.enemy
        self.speech = ""
        self.speechCounter = 0
        self.state = 0 if "quest-cactus-ended" in self.screen.saveData.tags else -1
        if (getCurMusic() == musicPath):
            self.animator.setAnimation("dancing")

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        dataSetter("x", self.X, "X")
        dataSetter("y", self.Y, "Y")
        dataSetter("color", self.color)

    def takeDamage(self, damage: int, attacker: Union[Entity, str, None] = None):
        if (not isinstance(attacker, Entity)):
            return
        if (self.animator.curAnimation().startswith("cactus") and attacker.id == "shovel"):
            if ("quest-cactus-started" not in self.screen.saveData.tags):
                return
            self.animator.setAnimation(f"appear{self.color}")
            self.animator.endDamageAnim()
            self.width = 0.5
            self.height = 0.6
            self.attackPushbackA = 0
            self.attackPushbackX = 0
            self.attackPushbackY = 0
            self.x = self.X + 0.17
            self.y = self.Y + 0.59
            if ("quest-cactus-ended" in self.screen.saveData.tags):
                self.state = 0
            elif (f"quest-cactus-{self.color}" not in self.screen.saveData.tags):
                self.state = 1
                self.screen.saveData.tags.append(f"quest-cactus-{self.color}")
            else:
                self.state = 2
        if (self.animator.curAnimation() == "stay" and self.state == 0):
            if (getCurMusic() != musicPath):
                self.animator.setAnimation("dancing")
                startMusicBreak(musicPath, 0.3)

    def update(self):
        super().update()
        if (self.animator.curAnimation().startswith("appear")):
            self.x = self.X + 0.17
            self.y = self.Y + 0.59 - self.animator.frame / 10
            if (self.animator.lastState[1]):
                self.x = self.X + 0.17
                self.y = self.Y + 0.59 - 0.4
                if (self.state == 0):
                    self.animator.setAnimation("dancing")
                    if (getCurMusic() != musicPath):
                        startMusicBreak(musicPath, 0.3)
                else:
                    self.animator.setAnimation("stay")
        elif (self.animator.curAnimation().startswith("cactus")):
            self.x = self.X
            self.y = self.Y
        else:
            self.x = self.X + 0.17
            self.y = self.Y + 0.59 - 0.4
        if (self.animator.curAnimation() == "stay"):
            if (self.state == 0):
                self.screen.player.message = TEXTS[0]
            elif (self.state == 1):
                self.screen.player.message = TEXTS[self.color]
            elif (self.state == 2):
                self.screen.player.message = TEXTS[5]
        elif (self.animator.curAnimation() == "dancing"):
            if (self.state == 0):
                self.screen.player.message = TEXTS[0]
            if (getCurMusic() != musicPath):
                self.animator.setAnimation(f"stay")


EntityAlive.registerEntity("cactusDancingChild", EntityCactusDancingChild)
