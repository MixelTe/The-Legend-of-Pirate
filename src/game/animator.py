import pygame


class AnimatorData:
    def init(self, folder: str, animations: list[tuple[str, int, tuple[int, int], tuple[int, int, int, int]]]):
        self.frames: dict[str, tuple[list[pygame.Surface], int, tuple[int, int]]] = {}
        # все кадры анимации, скорость переключения кадров (милисекунды между кадрами) и позиция картинки относительно сущности для каждой анимации

        # folder - папка с анимациями
        # animations - список tuple с содержимом:
            # [0] - название файла с анимацией
            # [1] - промежуток между кадрами (скорость переключения)
            # [2] - размер кадра в анимации
            # [3] - положение относительно сущности и требуемый размер кадра
        # Добавляет каждую анимацию в frames, разделив на кадры и применив масштаб imgSize. Ключ - название файла без расширения
        # Для каждой анимации в animations:
            # Делит картинку [0] на кадры размером [2]
            # Применяет масштаб [3] для каждого кадра
            # В frames[название_файла_без_расширения] кладёт tuple, с содержимым:
                # Список со всеми увеличеными кадрами
                # Промежуток между кадрами [1]
                # Положение кадра относительно сущности [3]

    def get_image(self, animation: str, index: int):
        return (self.frames[animation][0][index], self.frames[animation][2])

    def get_speed(self, animation: str):
        return self.frames[animation][1]


class Animator:
    def init(self, data: AnimatorData, frame: tuple[str, int]):
        self.data = data # все анимации и их кадры
        self.frame = frame # tuple[анимация, картинка] текущий кадр
        self.counter = 0 # счетчик для переключения кадров с определённой скоростью

    def update(self) -> tuple[bool, bool]:
        # прибавляет счётчик, и переключает кадр, если прошло достаточно времени. После последнего кадра идёт первый.
        # Возвращает два значения:
        # Был ли переключён кадр
        # Поледний ли это кадр анимации
        pass

    def getImage(self) -> tuple[pygame.Surface, tuple[int, int]]:
        # возвращает текущий кадр и его позицию относительно сущности
        pass

    def setAnimation(self, animation: str):
        # устанавливает текущую анимацию по её названию
        pass

    def curAnimation(self) -> str:
        # название текущей анимации
        pass
