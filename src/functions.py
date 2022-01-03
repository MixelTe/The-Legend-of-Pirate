import pygame
import os
from settings import Settings


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
