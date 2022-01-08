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

def load_entity(name: str, folder: str=None):
    if (folder is None):
        path = joinPath(Settings.folder_entities, name)
    else:
        path = joinPath(Settings.folder_entities, folder, name)
    return load_image(path)

def joinPath(*path: list[str]):
    return str(os.path.join(*path))


def createSprite(img: pygame.Surface, scale: int, group: pygame.sprite.Group, x=0, y=0):
    sprite = pygame.sprite.Sprite(group)
    scale = Settings.width * scale / img.get_width()
    sprite.rect = pygame.Rect(x * Settings.width, y * Settings.height, img.get_width() * scale, img.get_height() * scale)
    sprite.image = pygame.transform.scale(img, (sprite.rect.width, sprite.rect.height))
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


def multRect(rect: tuple[float, float, float, float], vw: float, vh: float=None):
    if (vh is None):
        vh = vw
    return pygame.Rect(rect[0] * vw, rect[1] * vh, rect[2] * vw, rect[3] * vh)


def multPos(pos: tuple[float, float], vw: float, vh: float=None):
    if (vh is None):
        vh = vw
    return (pos[0] * vw, pos[1] * vh)


def getRectMult(vw: float, vh: float=None):
    def mult(rect: tuple[float, float, float, float]):
        return multRect(rect, vw, vh)
    return mult


def getPosMult(vw: float, vh: float=None):
    def mult(pos: tuple[float, float]):
        return multPos(pos, vw, vh)
    return mult
