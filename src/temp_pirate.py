import pygame
from functions import load_image


class Pirate():
    image = load_image("pirate.png", -1)

    def __init__(self):
        scale = 8
        self.rect = pygame.Rect(500, 500, Pirate.image.get_width() * scale, Pirate.image.get_height() * scale)
        self.image = pygame.transform.scale(
            self.image, (self.rect.width, self.rect.height))
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

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
