import pygame
import os
import json
from settings import Settings


class GameExeption(Exception):
    pass


def load_image(name, color_key=None):
    fullname = joinPath(Settings.folder_data, Settings.folder_images, name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def joinPath(*path: list[str]):
    joined = path[0]
    for i in range(1, len(path)):
        joined = os.path.join(joined, path[i])
    return joined


def createSprite(img: pygame.Surface, scale: int, group: pygame.sprite.Group, x=0, y=0):
    sprite = pygame.sprite.Sprite(group)
    sprite.rect = pygame.Rect(x, y, img.get_width() * scale, img.get_height() * scale)
    sprite.image = pygame.transform.scale(img, (sprite.rect.width, sprite.rect.height))
    return sprite

def loadJSON(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def multRect(rect, value: float):
    rect[0] *= value
    rect[1] *= value
    rect[2] *= value
    rect[3] *= value
