from typing import Any, Callable, Union
from backMusic import getCurMusic, startMusicBreak
from functions import joinPath
from game.entity import Entity, EntityAlive, EntityGroups
from game.animator import Animator, AnimatorData
from settings import Settings


animatorData = AnimatorData("cactusDancing", [
    ("stay.png", 0, (18, 24), (-0.3, -0.9, 1.125, 1.5)),
    ("appear.png", 200, (18, 24), (-0.3, -0.9, 1.125, 1.5)),
    ("cactus.png", 0, (16, 16), (-0.075, -0.075, 1, 1)),
    ("dancing.png", 200, (20, 24), (-0.3625, -0.9, 1.25, 1.5)),
])
musicPath = joinPath(Settings.folder_data, Settings.folder_sounds, "back", "background2.mp3")
TEXTS = {
    0: "Привет, привет! Давай сыграем в игру? Найди четырёх моих братьев и получишь приз!",
    1: "Найди ещё четырёх моих братьев и получишь приз!",
    2: "Найди ещё троих моих братьев и получишь приз!",
    3: "Найди ещё двоих моих братьев и получишь приз!",
    4: "Найди ещё одного моего брата и получишь приз!",
    5: "Ты смог!!! Вот твоя награда!",
    6: "Спасибо за игру!",
}


class EntityCactusDancing(EntityAlive):
    def __init__(self, screen, data: dict = None):
        self.X = 0
        self.Y = 0
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "cactus")
        self.immortal = True
        self.width = 0.85
        self.height = 0.85
        self.group = EntityGroups.enemy
        self.speech = ""
        self.speechCounter = 0
        self.state = 0 if "quest-cactus-ended" in self.screen.saveData.tags else -1
        self.countFound = 0
        if (getCurMusic() == musicPath):
            self.animator.setAnimation("dancing")

    def applyData(self, dataSetter: Callable[[str, Any, str, Callable[[Any], Any]], None], data: dict):
        dataSetter("x", self.X, "X")
        dataSetter("y", self.Y, "Y")

    def takeDamage(self, damage: int, attacker: Union[Entity, str, None] = None):
        if (not isinstance(attacker, Entity)):
            return
        if (self.animator.curAnimation() == "cactus" and attacker.id == "shovel"):
            self.animator.setAnimation("appear")
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
            elif ("quest-cactus-started" not in self.screen.saveData.tags):
                self.state = 1
                self.screen.saveData.tags.append("quest-cactus-started")
            else:
                self.state = 2
                self.countFound = 0
                self.countFound += 1 if "quest-cactus-1" in self.screen.saveData.tags else 0
                self.countFound += 1 if "quest-cactus-2" in self.screen.saveData.tags else 0
                self.countFound += 1 if "quest-cactus-3" in self.screen.saveData.tags else 0
                self.countFound += 1 if "quest-cactus-4" in self.screen.saveData.tags else 0
                if (self.countFound == 4):
                    self.state = 3
                    self.screen.saveData.tags.append("quest-cactus-ended")
        if (self.animator.curAnimation() == "stay" and (self.state == 0 or self.state == 3)):
            if (getCurMusic() != musicPath):
                self.animator.setAnimation("dancing")
                startMusicBreak(musicPath, 0.3)

    def update(self):
        super().update()
        if (self.animator.curAnimation() == "appear"):
            self.x = self.X + 0.17
            self.y = self.Y + 0.59 - self.animator.frame / 10
            if (self.animator.lastState[1]):
                self.x = self.X + 0.17
                self.y = self.Y + 0.59 - 0.4
                if (self.state == 0 or self.state == 3):
                    self.animator.setAnimation("dancing")
                    if (getCurMusic() != musicPath):
                        startMusicBreak(musicPath, 0.3)
                else:
                    self.animator.setAnimation("stay")
        elif (self.animator.curAnimation() == "cactus"):
            self.x = self.X
            self.y = self.Y
        else:
            self.x = self.X + 0.17
            self.y = self.Y + 0.59 - 0.4
        if (self.animator.curAnimation() == "stay"):
            if (self.state == 0):
                self.screen.player.message = TEXTS[6]
            elif (self.state == 1):
                self.screen.player.message = TEXTS[0]
            elif (self.state == 2):
                self.screen.player.message = TEXTS[self.countFound + 1]
            elif (self.state == 3):
                self.screen.player.message = TEXTS[5]
        elif (self.animator.curAnimation() == "dancing"):
            if (self.state == 0):
                self.screen.player.message = TEXTS[6]
            elif (self.state == 3):
                self.screen.player.message = TEXTS[5]
            if (getCurMusic() != musicPath):
                self.animator.setAnimation("stay")


EntityAlive.registerEntity("cactusDancing", EntityCactusDancing)
