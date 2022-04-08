import pygame
from functions import rectPointIntersection
from settings import Settings
from window import Window
from game.entityPlayer import animatorData
from game.animator import Animator


class WindowAnimationTest(Window):
    def __init__(self):
        super().__init__()
        self.animators: list[Animator] = []
        self.drawRect = False
        self.size = [0, 0]
        self.size[0] = 0.55
        self.size[1] = 0.7
        self.cursor = (0, 0)
        for anim in animatorData.frames:
            animator = Animator(animatorData, anim)
            self.animators.append(animator)
        self.font = pygame.font.Font(Settings.path_font, int(Settings.tileSize * 0.8))

    def on_event(self, event: pygame.event.Event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_1):
                self.drawRect = not self.drawRect
        if (event.type == pygame.MOUSEMOTION):
            self.cursor = event.pos

    def update(self):
        for animator in self.animators:
            animator.update()

    def draw(self, screen: pygame.Surface):
        size = Settings.tileSize * 2
        lineW = screen.get_width() // size
        text = None
        for i, animator in enumerate(self.animators):
            x = i % lineW * size
            y = int(i / lineW) * size
            img, pos = animator.getImage()
            screen.blit(img, (x + pos[0] * Settings.tileSize + size / 2, y + pos[1] * Settings.tileSize + size / 2))
            if (self.drawRect):
                pygame.draw.rect(screen, "green", (x + size / 2, y + size / 2, self.size[0] * Settings.tileSize, self.size[1] * Settings.tileSize), 1)
            rect = (x, y, size, size)
            if (rectPointIntersection(rect, self.cursor)):
                text = animator.curAnimation()
        if (text and pygame.mouse.get_focused()):
            renderedText = self.font.render(text, True, "black")
            screen.blit(renderedText, ((screen.get_width() - renderedText.get_width()) // 2, screen.get_height() - Settings.tileSize * 0.9))

