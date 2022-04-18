import math
from random import choices
from typing import Callable, Union
import pygame
from functions import load_sound, rectPointIntersection
from game.animator import Animator, AnimatorData
from game.dialogs.map import GameDialog_map
from game.entity import Entity, EntityAlive, EntityGroups
from game.saveData import SaveData
from game.tile import Tile
from settings import Settings


animatorData = AnimatorData("pirate", [
    ("stayS.png", 0, (12, 24), (-0.1, -0.8, 0.75, 1.5)),
    ("stayW.png", 0, (12, 24), (-0.1, -0.8, 0.75, 1.5)),
    ("stayA.png", 0, (12, 18), (-0.25, -0.8, 1, 1.5)),
    ("stayD.png", 0, (12, 18), (-0.15, -0.8, 1, 1.5)),
    ("goingS.png", 150, (12, 24), (-0.1, -0.8, 0.75, 1.5)),
    ("goingW.png", 150, (12, 24), (-0.1, -0.8, 0.75, 1.5)),
    ("goingA.png", 150, (12, 18), (-0.25, -0.8, 1, 1.5)),
    ("goingD.png", 150, (12, 18), (-0.15, -0.8, 1, 1.5)),
    ("attackS.png", 100, (12, 32), (-0.1, -0.8, 0.75, 2)),
    ("attackW.png", 100, (12, 29), (-0.1, -1.1, 0.75, 1.8)),
    ("attackA.png", 100, (21, 18), (-1, -0.8, 1.75, 1.5)),
    ("attackD.png", 100, (21, 18), (-0.1, -0.8, 1.75, 1.5)),
    ("attack_swimS.png", 100, (18, 32), (-0.27, -0.9, 1.125, 2)),
    ("attack_swimW.png", 100, (18, 29), (-0.27, -1.1, 1.125, 1.8)),
    ("attack_swimA.png", 100, (21, 20), (-0.77, -0.9, 1.743, 1.66)),
    ("attack_swimD.png", 100, (20, 20), (-0.37, -0.9, 1.66, 1.66)),
    ("digD.png", 200, (21, 18), (-0.1, -0.8, 1.75, 1.5)),
    ("digA.png", 200, (21, 18), (-1.08, -0.8, 1.75, 1.5)),
    ("swimW.png", 0, (18, 24), (-0.27, -0.8, 1.125, 1.5)),
    ("swimS.png", 0, (18, 24), (-0.27, -0.8, 1.125, 1.5)),
    ("swimA.png", 0, (16, 18), (-0.37, -0.8, 1.33, 1.5)),
    ("swimD.png", 0, (16, 18), (-0.37, -0.8, 1.33, 1.5)),
    # ("swimingW.png", 150, (16, 24), (-0.1, -0.9, 1, 1.5)),
    # ("swimingS.png", 150, (16, 24), (-0.1, -0.9, 1, 1.5)),
    ("swimmingW.png", 150, (18, 24), (-0.27, -0.8, 1.125, 1.5)),
    ("swimmingS.png", 150, (18, 24), (-0.27, -0.8, 1.125, 1.5)),
    ("swimmingA.png", 150, (16, 18), (-0.37, -0.8, 1.33, 1.5)),
    ("swimmingD.png", 150, (16, 18), (-0.37, -0.8, 1.33, 1.5)),
    ("die.png", 800, (18, 24), (-0.28, -0.8, 1.125, 1.5)),
])

# sound_hit = load_sound("hit.wav")
# sound_walk = load_sound("walk.wav")
sound_hit = load_sound("attack_shovel.mp3")
sound_hit.set_volume(1.2)
sound_walk_sand = load_sound("walk3.mp3", "walk")
sound_walk = load_sound("walk2.wav", "walk")
sound_walk.set_volume(0.7)
sound_swim = load_sound("swing3.mp3", "swim")
sound_dig = load_sound("dig.mp3")


class EntityPlayer(EntityAlive):
    id = "player"

    def __init__(self, saveData: SaveData):
        super().__init__(None)
        self.saveData = saveData
        self.buttonPressed = []
        # нажаты ли кнопки движения в направлениях: вверх, вправо, вниз, влево (для корректного изменения направления движения)
        self.health = saveData.health
        self.healthMax = 8 if "heart-collected" in saveData.tags else 6
        self.group = EntityGroups.playerSelf
        self.weapon: Entity = None
        self.message = ""
        self.messageIsLong = False
        self.keyboardIsUsed = True
        self.speed = 0.06
        self.width = 0.55
        self.height = 0.7
        self.imagePos = (0, -0.5)
        self.x = saveData.checkPointX + (1 - self.width) / 2
        self.y = saveData.checkPointY + (1 - self.height) / 2
        self.animator = Animator(animatorData, "stayS")
        self.direction = "S"
        self.shovel = None
        self.state = "normal"
        self.action = None
        self.DamageDelay = Settings.damageDelayPlayer
        self.animator.DamageDelay = Settings.damageDelayPlayer
        self.animator.damageAnimCount = 4
        self.lastAttaker = ""
        self.walkSoundCounter = 0
        self.visibleForEnemies = True
        self.takeItemAnim = {"drawFun": None, "item": None, "onAnimEnd": None, "counter": 0, "size": (1, 1)}

    def onKeyDown(self, key):
        self.keyboardIsUsed = True
        if (key == pygame.K_w or key == pygame.K_UP):
            self.addKeyToPressed("up")
        if (key == pygame.K_s or key == pygame.K_DOWN):
            self.addKeyToPressed("down")
        if (key == pygame.K_d or key == pygame.K_RIGHT):
            self.addKeyToPressed("right")
        if (key == pygame.K_a or key == pygame.K_LEFT):
            self.addKeyToPressed("left")
        if (key == pygame.K_SPACE):
            self.attack()
        if (key == pygame.K_e):
            if (self.action):
                self.action()
            else:
                self.dig()

        if (Settings.moveScreenOnNumpad):
            if (key == pygame.K_KP_4):
                self.screen.tryGoTo("left")
            if (key == pygame.K_KP_8):
                self.screen.tryGoTo("up")
            if (key == pygame.K_KP_6):
                self.screen.tryGoTo("right")
            if (key == pygame.K_KP_2):
                self.screen.tryGoTo("down")

    def onKeyUp(self, key):
        self.keyboardIsUsed = True
        if (key == pygame.K_w or key == pygame.K_UP):
            self.removeKeyFromPressed("up")
        if (key == pygame.K_s or key == pygame.K_DOWN):
            self.removeKeyFromPressed("down")
        if (key == pygame.K_d or key == pygame.K_RIGHT):
            self.removeKeyFromPressed("right")
        if (key == pygame.K_a or key == pygame.K_LEFT):
            self.removeKeyFromPressed("left")
        if (key == pygame.K_q):
            self.openMap()

    def onJoyHat(self, value):
        self.keyboardIsUsed = False
        if (value[1] > 0):
            self.removeKeyFromPressed("down")
            self.addKeyToPressed("up")
        elif (value[1] < 0):
            self.removeKeyFromPressed("up")
            self.addKeyToPressed("down")
        else:
            self.removeKeyFromPressed("up")
            self.removeKeyFromPressed("down")
        if (value[0] > 0):
            self.removeKeyFromPressed("left")
            self.addKeyToPressed("right")
        elif (value[0] < 0):
            self.removeKeyFromPressed("right")
            self.addKeyToPressed("left")
        else:
            self.removeKeyFromPressed("right")
            self.removeKeyFromPressed("left")

    def onJoyAxis(self, axis, value):
        if (axis == 0):
            if (value > 0.5):
                self.keyboardIsUsed = False
                self.removeKeyFromPressed("left")
                self.addKeyToPressed("right")
            elif (value < -0.5):
                self.keyboardIsUsed = False
                self.removeKeyFromPressed("right")
                self.addKeyToPressed("left")
            else:
                self.removeKeyFromPressed("right")
                self.removeKeyFromPressed("left")
        elif (axis == 1):
            if (value > 0.5):
                self.keyboardIsUsed = False
                self.removeKeyFromPressed("up")
                self.addKeyToPressed("down")
            elif (value < -0.5):
                self.keyboardIsUsed = False
                self.removeKeyFromPressed("down")
                self.addKeyToPressed("up")
            else:
                self.removeKeyFromPressed("up")
                self.removeKeyFromPressed("down")
        elif (axis == 2):
            if (value > 0.5):
                self.keyboardIsUsed = False
                self.attack("D")
            elif (value < -0.5):
                self.keyboardIsUsed = False
                self.attack("A")
        elif (axis == 3):
            if (value > 0.5):
                self.keyboardIsUsed = False
                self.attack("S")
            elif (value < -0.5):
                self.keyboardIsUsed = False
                self.attack("W")

    def onJoyButonDown(self, button):
        self.keyboardIsUsed = False
        if (button == 2):
            self.attack()
        if (button == 1):
            if (self.action):
                self.action()
            else:
                self.dig()

    def addKeyToPressed(self, key):
        self.buttonPressed.append(key)

    def removeKeyFromPressed(self, key):
        while key in self.buttonPressed:
            self.buttonPressed.remove(key)

    def onJoyButonUp(self, button):
        if (button == 3):
            self.openMap()

    def setSpeed(self):
        self.speedX = 0
        self.speedY = 0
        if (self.state == "death" or self.state == "dead"):
            return
        if (self.state != "normal" and self.state != "swim" and self.state != "dig"):
            return
        if (len(self.buttonPressed) > 0):
            if (self.walkSoundCounter == 0):
                tile, _ = self.get_tile(pos=(0.5, 0.7))
                if (tile):
                    if ("water" in tile.tags):
                        sound_swim.play()
                    elif ("sand" in tile.tags):
                        sound_walk_sand.play()
                    else:
                        sound_walk.play()
            self.walkSoundCounter += 1000 / Settings.fps
            if (self.walkSoundCounter >= 350):
                self.walkSoundCounter = 0

            if (self.state == "dig"):
                self.state = "normal"
                sound_dig.stop()
            if (self.buttonPressed[-1] == "up"):
                self.speedY = -self.speed
                self.direction = "W"
            if (self.buttonPressed[-1] == "down"):
                self.speedY = self.speed
                self.direction = "S"
            if (self.buttonPressed[-1] == "right"):
                self.speedX = self.speed
                self.direction = "D"
            if (self.buttonPressed[-1] == "left"):
                self.speedX = -self.speed
                self.direction = "A"
        else:
            self.walkSoundCounter = 250
            sound_walk.stop()
            sound_walk_sand.stop()

    def attack(self, d=None):
        if (self.state != "normal" and self.state != "swim"):
            return
        if (d is not None):
            self.direction = d
        if (self.state == "swim"):
            self.state = "attack_swim"
        else:
            self.state = "attack"
        sound_hit.play()
        self.shovel = Entity.createById("shovel", self.screen)
        self.screen.addEntity(self.shovel)
        self.shovel.startX = self.x
        self.shovel.startY = self.y
        self.shovel.direction = self.direction
        self.shovel.nextStage()

    def dig(self):
        if (self.state != "normal"):
            return
        tileA, _ = self.get_tile(-1, pos=(0.5, 0.7))
        tileD, _ = self.get_tile(1, pos=(0.2, 0.7))
        if (self.direction == "A" and tileA and tileA.digable):
            tile = tileA
        elif (self.direction != "A" and tileD and tileD.digable):
            tile = tileD
            self.direction = "D"
        elif (tileD and tileD.digable):
            tile = tileD
            self.direction = "D"
        elif (tileA and tileA.digable):
            tile = tileA
            self.direction = "A"
        if (tile and tile.digable):
            self.state = "dig"
            sound_dig.play()

    def afterDig(self):
        if (self.direction == "A"):
            entities = self.get_entitiesD((-0.75, 0.4, 0.4, 0.3))
        else:
            entities = self.get_entitiesD((0.9, 0.4, 0.4, 0.3))
        dig_place = None
        dig_place_hidden = None
        for e in entities:
            if e.id == "dig_place":
                if (not e.digged):
                    dig_place = e
                    break
            if e.id == "dig_place_hidden":
                dig_place_hidden = e
                break

        if (dig_place_hidden):
            dig_place_hidden.dig()

        if (dig_place and not dig_place.digged):
            dig_place.dig()
            options = ["coin", "heart", "crab"]
            if (dig_place.content in options):
                found = dig_place.content
            else:
                found = choices(options, [0.5, 0.4, 0.1])[0]
            entity = Entity.createById(found, self.screen)
            self.screen.addEntity(entity)
            dx, dy = (-0.6, 0.5) if self.direction == "A" else (1.1, 0.5)
            entity.x = self.x + dx - entity.width / 2
            entity.y = self.y + dy - entity.height / 2

    def openMap(self):
        if ("quest-pirate-ended" in self.saveData.tags or "quest-cactus-ended" in self.saveData.tags):
            parts = 0
            parts += 1 if "quest-pirate-ended" in self.saveData.tags else 0
            parts += 1 if "quest-cactus-ended" in self.saveData.tags else 0
            self.screen.openDialog(GameDialog_map(parts))

    def update(self):
        self.setSpeed()
        super().update()
        self.takeItemAnim["counter"] = min(2, self.takeItemAnim["counter"] + 0.01)
        if (self.takeItemAnim["counter"] == 2):
            self.takeItemAnim["drawFun"] = None
            self.takeItemAnim["item"] = None
            if (self.takeItemAnim["onAnimEnd"]):
                self.takeItemAnim["onAnimEnd"]()
                self.takeItemAnim["onAnimEnd"] = None

        if (self.state == "dig"):
            self.animator.setAnimation("digA" if self.direction == "A" else "digD")
            if (self.animator.lastState[1]):
                self.afterDig()
                self.state = "normal"
            if (self.animator.lastState[0]):
                sound_walk.play()
        elif (self.state == "death"):
            if (self.animator.lastState[1]):
                self.animator.setAnimation("die", 3)
                self.state = "dead"
        elif (self.state == "dead"):
            self.animator.setAnimation("die", 3)
        elif (self.state == "attack" or self.state == "attack_swim"):
            if (self.shovel is not None):
                self.animator.setAnimation(self.state + self.direction)
                if (self.animator.lastState[1]):
                    self.shovel.remove()
                    self.shovel = None
                    self.state = "normal"
                elif (self.animator.lastState[0]):
                    self.shovel.nextStage()
        else:
            tile, _ = self.get_tile(pos=(0.5, 0.7))
            swim = False
            if (tile and "water" in tile.tags):
                x, y = self.x + self.width * 0.5, self.y + self.height * 0.7
                zone = [int(x), int(y), 1, 1]
                swim = rectPointIntersection(zone, (x, y))
            if (swim):
                self.state = "swim"
                anim = "swim" if self.speedX == 0 and self.speedY == 0 else "swimming"
                self.animator.setAnimation(anim + self.direction)
            else:
                self.state = "normal"
                anim = "stay" if self.speedX == 0 and self.speedY == 0 else "going"
                self.animator.setAnimation(anim + self.direction)

        if (self.x <= 0.05):
            if (self.screen.tryGoTo("left")):
                self.x = Settings.screen_width - self.width - 0.1
        elif (self.x + self.width >= Settings.screen_width - 0.05):
            if (self.screen.tryGoTo("right")):
                self.x = 0.1
        elif (self.y <= 0.05):
            if (self.screen.tryGoTo("up")):
                self.y = Settings.screen_height - self.height - 0.1
        elif (self.y + self.height >= Settings.screen_height - 0.05):
            if (self.screen.tryGoTo("down")):
                self.y = 0.1

        if (Settings.ghostmode):
            self.hidden = True
            self.ghostE = True
            self.ghostE = True
            self.immortal = True
            self.visibleForEnemies = False
        elif (self.hidden):
            self.hidden = False
            self.ghostE = False
            self.ghostE = False
            self.immortal = False
            self.visibleForEnemies = True
        if (not Settings.ghostmode):
            entities = self.get_entitiesD((0, self.height * 0.9, self.width, self.height * 0.1))
            self.visibleForEnemies = True
            for entity in entities:
                if (entity.id == "bush"):
                    self.visibleForEnemies = False
                    break
        else:
            a = 1
        # self.animator.setAnimation("attack_swimS")

    def preUpdate(self):
        self.message = ""
        self.messageIsLong = False
        self.action = None

    def takeDamage(self, damage: int, attacker: Union[Entity, str, None] = None):
        if (super().takeDamage(damage, attacker)):
            if (isinstance(attacker, Entity)):
                self.lastAttaker = attacker.id
            if (isinstance(attacker, str)):
                self.lastAttaker = attacker

    def centerTo(self, pos: tuple[int, int]):
        self.x = pos[0] + (1 - self.width) / 2
        self.y = pos[1] + (1 - self.height) / 2

    def canGoOn(self, tile: Tile) -> bool:
        if (Settings.ghostmode):
            return True
        return super().canGoOn(tile)

    def draw(self, surface: pygame.Surface):
        self.drawItemTaking(surface)
        if (not self.visibleForEnemies):
            return super().draw(surface, 0.7)
        return super().draw(surface)

    def death(self):
        self.state = "death"
        self.animator.setAnimation("die")

    def takeItem(self, item: Entity, onAnimEnd: Callable[[], None] = None):
        self.takeItemAnim["item"] = item
        self.takeItemAnim["onAnimEnd"] = onAnimEnd
        self.takeItemAnim["counter"] = 0

    def takeItemFun(self, size: tuple[float, float], drawFun: Callable[[pygame.Surface, float, float, float], None], onAnimEnd: Callable[[], None] = None):
        self.takeItemAnim["drawFun"] = drawFun
        self.takeItemAnim["onAnimEnd"] = onAnimEnd
        self.takeItemAnim["size"] = size
        self.takeItemAnim["counter"] = 0

    def drawItemTaking(self, surface: pygame.Surface):
        drawFun = self.takeItemAnim["drawFun"]
        item = self.takeItemAnim["item"]
        if (not drawFun and not item):
            return
        counter = self.takeItemAnim["counter"] / 2
        w, h = self.takeItemAnim["size"]
        if (item):
            w = item.width
            h = item.height
        x = self.x + self.width / 2 - w / 2
        if (counter < 0.4):
            y = self.y - h - 0.8 - counter
            s = 1
        else:
            counter -= 0.4
            v = counter / 0.6
            y = self.y - h - 1.3 + counter * 1.2
            s = 1 - max(0, v - 0.2)
        drawItemTakingBorder(surface, x, y, w, h, counter, s)
        x += w * (1 - s) / 2
        y += h * (1 - s) / 2
        if (drawFun):
            drawFun(surface, x, y, s)
        else:
            drawItemTaking(item, surface, x, y, s)


def drawItemTakingBorder(surface: pygame.Surface, x: float, y: float, w: float, h: float, counter: float, s: float):
    x, y = x * Settings.tileSize, y * Settings.tileSize
    w, h = w * Settings.tileSize, h * Settings.tileSize
    size = (max(w, h) + 40)
    sizeCircle = (size - 20) / 2
    sizeCircleSmall = sizeCircle * 0.4
    size *= s
    sizeCircle *= s
    sizeCircleSmall *= s
    img = pygame.Surface((size, size), pygame.SRCALPHA)
    img.fill((0, 0, 0, 0))
    pygame.draw.circle(img, pygame.Color(255, 255, 135), (size / 2, size / 2), sizeCircle)
    count = 5
    step = math.pi * 2 / count
    offset = counter * math.pi * 2
    for i in range(count):
        X = math.cos(step * i + offset) * sizeCircle + size / 2
        Y = math.sin(step * i + offset) * sizeCircle + size / 2
        pygame.draw.circle(img, pygame.Color(255, 108, 79), (X, Y), sizeCircleSmall)
    img.fill((255, 255, 255, 180), None, pygame.BLEND_RGBA_MULT)
    surface.blit(img, (x - (size - w) / 2, y - (size - h) / 2))


def drawItemTaking(item: Entity, surface: pygame.Surface, x: float, y: float, s: float):
    image = item.image
    if (not image):
        return
    size = image.get_size()
    if (s != 1):
        size = (size[0] * s, size[1] * s)
        image = pygame.transform.scale(image, size)
    surface.blit(image, (x * Settings.tileSize, y * Settings.tileSize))
