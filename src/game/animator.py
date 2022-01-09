import pygame

from functions import load_entity
from settings import Settings


class AnimatorData:
    def __init__(self, folder: str, animations: list[tuple[str, int, tuple[int, int], tuple[float, float, float, float]]]):
        self.frames: dict[str, tuple[list[pygame.Surface], int, tuple[int, int]]] = {}
        # все кадры анимации, скорость переключения кадров (милисекунды между кадрами) и позиция картинки относительно сущности для каждой анимации

        for imgName, speed, frameSize, imgRect in animations:
            animName = imgName[:imgName.index(".")]
            allFrames = load_entity(imgName, folder)
            frames = []
            count = allFrames.get_width() // frameSize[0]
            for x in range(count):
                frame = allFrames.subsurface(x * frameSize[0], 0, *frameSize)
                frame = pygame.transform.scale(frame, (imgRect[2] * Settings.tileSize, imgRect[3] * Settings.tileSize))
                frames.append(frame)
            self.frames[animName] = (frames, speed, (imgRect[0], imgRect[1]))

    def get_image(self, animation: str, index: int):
        return (self.frames[animation][0][index], self.frames[animation][2])

    def get_speed(self, animation: str):
        return self.frames[animation][1]

    def get_len(self, animation: str):
        return len(self.frames[animation][0])


class Animator:
    def __init__(self, data: AnimatorData, anim: str):
        self.data = data # все анимации и их кадры
        self.anim = anim # текущая анимация
        self.frame = 0 # текущий кадр
        self.counter = 0 # счетчик для переключения кадров с определённой скоростью

    def update(self) -> tuple[bool, bool]:
        self.counter += 1000 / Settings.fps
        if (self.counter > self.data.get_speed(self.anim)):
            self.counter = 0
            self.frame += 1
            self.frame = self.frame % self.data.get_len(self.anim)
            return (True, self.frame == 0)
        # Возвращает два значения:
        # Был ли переключён кадр
        # Поледний ли был кадр анимации
        return (False, False)

    def getImage(self) -> tuple[pygame.Surface, tuple[int, int]]:
        return self.data.get_image(self.anim, self.frame)

    def setAnimation(self, animation: str):
        self.anim = animation
        self.frame = 0

    def curAnimation(self) -> str:
        return self.anim
