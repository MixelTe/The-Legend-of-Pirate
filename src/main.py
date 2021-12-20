import pygame
import os
import sys

size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data\images', name)
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


class Pirate(pygame.sprite.Sprite):
    image = load_image("pirate.png", -1)

    def __init__(self):
        super().__init__(all_sprites)

        self.image = Pirate.image
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = 500
        self.rect.y = 500
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed


class Main:
    def __init__(self):

        self.all_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        Pirate()
        self.running = True

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            screen.fill((0, 0, 0))
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()



if (__name__ == "__main__"):
    Main().start()