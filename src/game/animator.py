import pygame
from typing import Union


class Animator:
    def init(self, image: pygame.Surface, frameSize: tuple[int, int], animation: list[int, int]):
        self.image = image # картинка с анимациями, каждая анимация на новой строке
        self.frameSize = frameSize
        self.animation = animation # tuple[скорость переключения кадров, кол-во кадров] для каждой анимации.
        self.frame = (0, 0) # tuple[строка, картинка]
        self.counter = 0 # счетчик для переключения кадров с определённой скоростью
        self.names: list[str] = [] # названия анимаций

    def setNames(self, names: list[str]):
        # - устанавливает название для каждой анимации
        pass

    def update(self) -> tuple[bool, bool]:
        # прибавляет счётчик, и переключает кадр, если прошло достаточно времени. После последнего кадра идёт первый.
        # Возвращает два значения:
        # Был ли переключён кадр
        # Поледний ли это кадр анимации
        pass

    def getImage(self) -> pygame.Surface:
        # возвращает текущий кадр
        pass

    def setAnimation(self, animation: Union[int, str]):
        # устанавливает текущую анимацию по номеру или её названию
        pass

    def curAnimation(self) -> tuple[int, Union[str, None]]:
        # номер и название (если есть, иначе None) текущей анимации
        pass
