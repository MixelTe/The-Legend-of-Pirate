import pygame
from window import Window
from functions import load_image


class WindowStart(Window):
    image_start = load_image("start.png", -1)
    image_quit = load_image("quit.png", -1)

    def __init__(self):
        self.quit_size = []

        scale = 12
        self.rect_start = pygame.Rect(750, 200, WindowStart.image_start.get_width() * scale, WindowStart.image_start.get_height() * scale)
        self.image_start = pygame.transform.scale(self.image_start, (self.rect_start.width, self.rect_start.height))
        
        self.rect_quit = pygame.Rect(750, 400, WindowStart.image_quit.get_width() * scale, WindowStart.image_quit.get_height() * scale)
        self.image_quit = pygame.transform.scale(self.image_quit, (self.rect_quit.width, self.rect_quit.height))

        for i in range(750, 750 + self.rect_quit.width):
            for j in range(400, 400 + self.rect_quit.height):
                self.quit_size.append([i, j])

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image_start, self.rect_start)
        screen.blit(self.image_quit, self.rect_quit)

    def quit_game(self, pos):
        if [pos[0], pos[1]] in self.quit_size:
            pygame.quit()