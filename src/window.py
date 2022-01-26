import pygame

from functions import load_image, load_sound
from settings import Settings


class Window():
    def on_event(self, event: pygame.event.Event):
        pass

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        pass


sound_btn = load_sound("btn1.mp3", "btn")
sound_btn2 = load_sound("btn2.wav", "btn")


class WindowWithButtons(Window):
    background = pygame.transform.scale(load_image("background.png"), (Settings.width, Settings.height))

    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.selected = 0

    def update(self):
        for sprite in self.all_sprites:
            sprite.active = False
        if (self.selected >= 0):
            self.all_sprites.sprites()[self.selected].active = True
        self.all_sprites.update()

    def action(self):
        pass

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.action()
            sound_btn.play()
        elif (event.type == pygame.MOUSEMOTION):
            selected = self.selected
            self.selected = -1
            for i, sprite in enumerate(self.all_sprites):
                if sprite.rect.collidepoint(event.pos):
                    self.selected = i
                    if (selected != i):
                        sound_btn2.play()
        elif (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_s or event.key == pygame.K_DOWN
                    or event.key == pygame.K_d or event.key == pygame.K_RIGHT):
                self.selected = ((self.selected + 1) + len(self.all_sprites)) % len(self.all_sprites)
                sound_btn2.play()
            if (event.key == pygame.K_w or event.key == pygame.K_UP
                    or event.key == pygame.K_a or event.key == pygame.K_LEFT):
                self.selected = ((self.selected - 1) + len(self.all_sprites)) % len(self.all_sprites)
                sound_btn2.play()
        elif (event.type == pygame.KEYUP):
            if (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                self.action()
                sound_btn.play()
        elif (event.type == pygame.JOYHATMOTION):
            if (event.value[1] < 0 or event.value[0] > 0):
                self.selected = ((self.selected + 1) + len(self.all_sprites)) % len(self.all_sprites)
                sound_btn2.play()
            if (event.value[1] > 0 or event.value[0] < 0):
                self.selected = ((self.selected - 1) + len(self.all_sprites)) % len(self.all_sprites)
                sound_btn2.play()
        elif (event.type == pygame.JOYBUTTONUP):
            if (event.button == 0):
                self.action()
                sound_btn.play()

    def draw(self, screen: pygame.Surface):
        screen.blit(WindowWithButtons.background, (0, 0))
        self.all_sprites.draw(screen)
