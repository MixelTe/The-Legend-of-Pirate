import math
from typing import Literal, Union
import pygame
import os
import json
from settings import Settings
from random import random


class GameExeption(Exception):
    pass


def load_image(name: str, color_key=None):
    fullname = joinPath(Settings.folder_data, Settings.folder_images, name)
    try:
        image = pygame.image.load(fullname)
    except Exception as message:
        raise GameExeption(f'Cannot load image: {name}\n{message}')

    if color_key is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)

    return image


def load_tile(name: str):
    return load_image(joinPath(Settings.folder_tiles, name))


def load_entity(name: str, folder: str = None):
    if (folder is None):
        path = joinPath(Settings.folder_entities, name)
    else:
        path = joinPath(Settings.folder_entities, folder, name)
    return load_image(path)


def load_decor(name: str, folder: str = None):
    if (folder is None):
        path = joinPath(Settings.folder_decor, name)
    else:
        path = joinPath(Settings.folder_decor, folder, name)
    return load_image(path)


def load_entityImg(name: str, w: float, h: float):
    return scaleImg(load_entity(name), w, h)


def load_entityStay(name: str, orig_w: float, orig_h: float, w: float, h: float):
    return scaleImg(load_entity("stay.png", name).subsurface(0, 0, orig_w, orig_h), w, h)


def scaleImg(img: pygame.Surface, w: float, h: float):
    return pygame.transform.scale(img, (int(Settings.tileSize * w), int(Settings.tileSize * h)))


def joinPath(*path: list[str]):
    return str(os.path.join(*path))


def load_sound(name: str, folder: str = None):
    if (folder):
        path = joinPath(Settings.folder_data, Settings.folder_sounds, folder, name)
    else:
        path = joinPath(Settings.folder_data, Settings.folder_sounds, name)
    return pygame.mixer.Sound(path)


class Button(pygame.sprite.Sprite):
    def __init__(self, group, img, img_a):
        super().__init__(group)
        self.img = img
        self.img_a = img_a
        self.active = False
        self.image = self.img

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.image = self.img_a if (self.active) else self.img


def createButton(imgName: str, scale: int, group: pygame.sprite.Group, x=0, y=0):
    img = load_image(imgName + ".png")
    img_a = load_image(imgName + "_active.png")
    scale = Settings.width * scale / img.get_width()
    w, h = int(img.get_width() * scale), int(img.get_height() * scale)
    img = pygame.transform.scale(img, (w, h))
    img_a = pygame.transform.scale(img_a, (w, h))
    sprite = Button(group, img, img_a)
    sprite.rect = pygame.Rect(x * Settings.width, y * Settings.height, w,  h)
    return sprite


def loadJSON(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def rectIntersection(rect1: tuple[float, float, float, float], rect2: tuple[float, float, float, float]):
    return (
        rect1[0] + rect1[2] > rect2[0] and
        rect2[0] + rect2[2] > rect1[0] and
        rect1[1] + rect1[3] > rect2[1] and
        rect2[1] + rect2[3] > rect1[1]
    )


def rectPointIntersection(rect1: tuple[float, float, float, float], point: tuple[float, float]):
    return (
        rect1[0] + rect1[2] > point[0] and
        rect1[1] + rect1[3] > point[1] and
        point[0] > rect1[0] and
        point[1] > rect1[1]
    )


def multRect(rect: tuple[float, float, float, float], vw: float, vh: float = None):
    if (vh is None):
        vh = vw
    return pygame.Rect(rect[0] * vw, rect[1] * vh, rect[2] * vw, rect[3] * vh)


def multPos(pos: tuple[float, float], vw: float, vh: float = None):
    if (vh is None):
        vh = vw
    return (pos[0] * vw, pos[1] * vh)


def getRectMult(vw: float, vh: float = None):
    def mult(rect: tuple[float, float, float, float]):
        return multRect(rect, vw, vh)
    return mult


def getPosMult(vw: float, vh: float = None):
    def mult(pos: tuple[float, float]):
        return multPos(pos, vw, vh)
    return mult


def renderText(font: pygame.font.Font, lineHeight: int, size: tuple[int, int], text: str, color: Union[str, pygame.Color], centerX=False, centerY=False):
    lines = renderText_split(font, size, text)
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill(pygame.Color(0, 0, 0, 0))
    displayLines(surface, font, lineHeight, (0, 0), lines, color, centerX, centerY)
    return surface


def renderText_split(font: pygame.font.Font, size: tuple[int, int], text: str):
    lines = []
    line = ""
    for word in text.split():
        newLine = line + " " + word
        if (font.size(newLine)[0] <= size[0]):
            line = newLine
        else:
            lines.append(line)
            line = word
    if (line != ""):
        lines.append(line)
    if (len(lines) >= 1):
        lines[0] = lines[0][1:]
    return lines


def displayLines(surface: pygame.Surface, font: pygame.font.Font, lineHeight: int, pos: tuple[int, int], lines: list[str], color: Union[str, pygame.Color], centerX=False, centerY=False):
    dy = (surface.get_height() - len(lines) * lineHeight) // 2 if centerY else 0
    y = pos[1] + dy

    def writeLine(text: str):
        nonlocal y
        text_img = font.render(text, True, color)
        dx = (surface.get_width() - text_img.get_width()) // 2 if centerX else 0
        surface.blit(text_img, (pos[0] + dx, y))
        y += lineHeight

    for line in lines:
        writeLine(line)


class TextAnimator:
    def __init__(self, font: pygame.font.Font, lineHeight: int, size: tuple[int, int], text: str, color: Union[str, pygame.Color], centerX=False, centerY=False):
        self.font = font
        self.lineHeight = lineHeight
        self.color = color
        self.centerX = centerX
        self.centerY = centerY
        self.lines = renderText_split(font, size, text)
        self.curLines = []
        self.curLine = 0
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.counter = 0
        self.stop = False

    def draw(self):
        self.surface.fill(pygame.Color(0, 0, 0, 0))
        displayLines(self.surface, self.font, self.lineHeight, (0, 0),
                     self.curLines, self.color, self.centerX, self.centerY)
        return self.surface

    def update(self):
        if (self.stop):
            return
        self.counter -= 1000 / Settings.fps

        if (self.counter <= 0):
            if (len(self.curLines) <= self.curLine):
                self.curLines.append("")
            curL = len(self.curLines[self.curLine])
            if (len(self.lines[self.curLine]) > curL):
                ch = self.lines[self.curLine][curL]
                self.curLines[self.curLine] += ch
                if (ch == " "):
                    self.counter = 80
                elif (ch == ","):
                    self.counter = 300
                elif (ch == "."):
                    self.counter = 400
                else:
                    self.counter = 50
            else:
                self.curLine += 1
                curL = 0
                if (len(self.lines) <= self.curLine):
                    self.stop = True

    def toEnd(self):
        self.stop == True
        self.curLines = self.lines


def removeFromCollisions(collisions: list, entitiesId: list[str], entitiesTags: list[str] = []):
    from game.entity import Entity
    for i in range(len(collisions) - 1, -1, -1):
        rect, obj = collisions[i]
        if (isinstance(obj, Entity)):
            if (obj.id in entitiesId):
                collisions.pop(i)
                continue
            for tag in obj.tags:
                if (tag in entitiesTags):
                    collisions.pop(i)
                    break


def compare(a: float, sign: Union[Literal["=="], Literal[">="], Literal["<="]], b: float):
    isEqual = abs(a - b) < 0.00001
    if (sign == ">="):
        return isEqual or a > b
    if (sign == "<="):
        return isEqual or a < b
    return isEqual


def distanceRects(r1: tuple[float, float, float, float], r2: tuple[float, float, float, float], center=True, sqrt=False):
    if (center):
        dx = (r1[0] + r1[2] / 2) - (r2[0] + r2[2] / 2)
        dy = (r1[1] + r1[3] / 2) - (r2[1] + r2[3] / 2)
    else:
        dx = r1[0] - r2[0]
        dy = r1[1] - r2[1]
    d = dx * dx + dy * dy
    if (sqrt):
        d = d ** 0.5
    return d


def drawPie(surface: pygame.Surface, color: pygame.Color, center: tuple[int, int], r: int, startA: float, endA: float, width=0, q=15, alpha=False):
    cx, cy = center
    cx, cy = int(cx), int(cy)
    startA = int(startA * 180 / math.pi)
    endA = int(endA * 180 / math.pi)
    if (startA > endA):
        startA, endA = endA, startA

    if (alpha):
        p = [(r, r)]
        for n in range(startA, endA + 1, q):
            x = r + int(r * math.cos(n * math.pi / 180))
            y = r + int(r * math.sin(n * math.pi / 180))
            p.append((x, y))
        p.append((
            r + int(r * math.cos((endA + 1) * math.pi / 180)),
            r + int(r * math.sin((endA + 1) * math.pi / 180))))
        p.append((r, r))
    else:
        p = [(cx, cy)]
        for n in range(startA, endA + 1, q):
            x = cx + int(r * math.cos(n * math.pi / 180))
            y = cy + int(r * math.sin(n * math.pi / 180))
            p.append((x, y))
        p.append((
            cx + int(r * math.cos((endA + 1) * math.pi / 180)),
            cy + int(r * math.sin((endA + 1) * math.pi / 180))))
        p.append((cx, cy))

    if len(p) > 3:
        if (alpha):
            surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.polygon(surf, color, p, width)
            surface.blit(surf, (cx - r, cy - r))
        else:
            pygame.draw.polygon(surface, color, p, width)


def distance(e1, e2):
    return (e1.x + e1.width / 2) - (e2.x + e2.width / 2), (e1.y + e1.height / 2) - (e2.y + e2.height / 2)


def dropCoin(self):
    if (random() < 0.5):
        return
    from game.entity import Entity
    self: Entity = self
    coin = Entity.createById("coin", self.screen)
    coin.x = self.x + self.width / 2
    coin.y = self.y + self.height / 2
    self.screen.addEntity(coin)


def calcPlayerCoinsAfterDeath(tags: list[str], coins: int):
    coinbagCount = 0
    coinbagCount += 1 if "coinbag-1" in tags else 0
    coinbagCount += 1 if "coinbag-2" in tags else 0
    coinbagCount += 1 if "coinbag-3" in tags else 0
    if (coinbagCount == 0):
        return 0
    elif (coinbagCount == 1):
        return int(coins * 0.25)
    elif (coinbagCount == 2):
        return int(coins * 0.5)
    else:
        return int(coins * 0.75)
