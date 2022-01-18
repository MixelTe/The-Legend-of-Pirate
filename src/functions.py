from typing import Union
import pygame
import os
import json
from settings import Settings


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


def load_entityImg(name: str, w: float, h: float):
    return scaleImg(load_entity(name), w, h)


def load_entityStay(name: str, orig_w: float, orig_h: float, w: float, h: float):
    return scaleImg(load_entity("stay.png", name).subsurface(0, 0, orig_w, orig_h), w, h)


def scaleImg(img: pygame.Surface, w: float, h: float):
    return pygame.transform.scale(img, (Settings.tileSize * w, Settings.tileSize * h))


def joinPath(*path: list[str]):
    return str(os.path.join(*path))


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
    w, h = img.get_width() * scale, img.get_height() * scale
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


def renderText(font: pygame.font.Font, lineHeight: int, size: tuple[int, int], text: str, color: Union[str, pygame.Color]):
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
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill(pygame.Color(0, 0, 0, 0))
    displayLines(surface, font, lineHeight, (0, 0), lines, color)
    return surface


def displayLines(surface: pygame.Surface, font: pygame.font.Font, lineHeight: int, pos: tuple[int, int], lines: list[str], color: Union[str, pygame.Color]):
    y = pos[1]

    def writeLine(text: str):
        nonlocal y
        text_img = font.render(text, True, color)
        surface.blit(text_img, (pos[0], y))
        y += lineHeight

    for line in lines:
        writeLine(line)
