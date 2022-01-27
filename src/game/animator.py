import pygame
from functions import GameExeption, load_entity
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
                frame = pygame.transform.scale(frame, (int(imgRect[2] * Settings.tileSize), int(imgRect[3] * Settings.tileSize)))
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
        self.data = data  # все анимации и их кадры
        self.anim = anim  # текущая анимация
        self.frame = 0  # текущий кадр
        self.counter = 0  # счетчик для переключения кадров с определённой скоростью
        self.lastState = (False, False)
        self.damageAnim = False
        self.damageAnimFinished = False
        self.damageAnimCounter = 0
        self.damageAnimCount = 1
        self.DamageDelay = Settings.damageDelay

    def update(self) -> tuple[bool, bool]:
        self.counter += 1000 / Settings.fps
        if (self.damageAnim):
            self.damageAnimCounter = self.damageAnimCounter + 1000 // Settings.fps
            if (self.damageAnimCounter >= self.DamageDelay):
                self.endDamageAnim()
        if (self.counter > self.data.get_speed(self.anim)):
            self.counter = 0
            self.frame += 1
            self.frame = self.frame % self.data.get_len(self.anim)
            self.lastState = (True, self.frame == 0)
            return self.lastState
        # Возвращает два значения:
        # Был ли переключён кадр
        # Поледний ли был кадр анимации
        self.lastState = (False, False)
        return self.lastState

    def getImage(self) -> tuple[pygame.Surface, tuple[int, int]]:
        imgD = self.data.get_image(self.anim, self.frame)
        if (not self.damageAnim):
            return imgD
        if (self.damageAnimCounter % (self.DamageDelay // self.damageAnimCount) < self.DamageDelay // (self.damageAnimCount * 2)):
            return imgD
        img = imgD[0].copy()
        v = 128
        img.fill((v, v, v), special_flags=pygame.BLEND_RGB_ADD)
        return (img, imgD[1])

    def setAnimation(self, animation: str, frame: int = None):
        if (animation not in self.data.frames):
            raise GameExeption(f"Animator.setAnimation: No such animation: {animation}")
        if (frame is None):
            if (animation != self.anim):
                self.frame = 0
                self.lastState = (False, self.frame == self.data.get_len(animation) - 1)
        else:
            self.frame = frame
            self.lastState = (True, self.frame == self.data.get_len(animation) - 1)
        self.anim = animation

    def curAnimation(self) -> str:
        return self.anim

    def startDamageAnim(self):
        self.damageAnimCounter = 0
        self.damageAnim = True
        self.damageAnimFinished = False

    def endDamageAnim(self):
        self.damageAnimCounter = 0
        self.damageAnim = False
        self.damageAnimFinished = True