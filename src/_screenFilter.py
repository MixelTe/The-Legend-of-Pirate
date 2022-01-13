import pygame


V = 0
vv = 1


def aplly(screen: pygame.Surface):
    global V, vv
    V += vv
    if (V > 70 or V <= 0):
        vv *= -1
    v = min(V, 50)
    if (v <= 3):
        return
    w, h = screen.get_width(), screen.get_height()
    for y in range(0, h, v):
        for x in range(0, w, v):
            pixel = screen.get_at((x, y))
            pygame.draw.rect(screen, pixel, (x - v // 2, y - v // 2, v, v))
            # pygame.draw.rect(screen, pixel, (x, y, v, v))
        pixel = screen.get_at((w - 1, y))
        pygame.draw.rect(screen, pixel, (w - 1 - v // 2, y - v // 2, v, v))
    pixel = screen.get_at((w - 1, h - 1))
    pygame.draw.rect(screen, pixel, (w - 1 - v // 2, h - 1 - v // 2, v, v))
