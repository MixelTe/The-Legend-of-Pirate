import pygame

image_cell: pygame.Surface = None
image_pirate: pygame.Surface = None
image_pirate2: pygame.Surface = None
image_pirate3: pygame.Surface = None


class Board:
    def __init__(self):
        self.cellsize = 128
        # self.width = 1920 // self.cellsize
        # self.height = 1080 // self.cellsize - 1
        self.width = 15
        self.height = 7
        self.top = 1080 - self.height * self.cellsize
        self.font = pygame.font.Font(None, 30)

    def draw(self, screen: pygame.Surface):
        for y in range(self.height):
            for x in range(self.width):
                rect = (
                    x * self.cellsize,
                    y * self.cellsize + self.top,
                    self.cellsize,
                    self.cellsize
                )
                # pygame.draw.rect(screen, "lightblue", rect, 2)
                screen.blit(pygame.transform.scale(
                    image_cell, (self.cellsize, self.cellsize)), (rect[0], rect[1]))
                text = self.font.render(f"{x}:{y}", True, "black")
                screen.blit(text, (rect[0] + 10, rect[1] + 10))


class Pirate:
    def __init__(self):
        self.scale = 128 / 16
        self.width = image_pirate.get_width() * self.scale
        self.height = image_pirate.get_height() * self.scale
        self.x = 0
        self.y = 1080 - 7 * 128 - self.height
        self.image = image_pirate
        self.speedX = 0
        self.speedY = 0

    def draw(self, screen: pygame.Surface):
        screen.blit(pygame.transform.scale(
            self.image, (self.width, self.height)), (self.x, self.y))

    def update(self):
        self.y += self.speedY
        self.x += self.speedX
        if (self.speedY < 0):
            self.image = image_pirate3
        if (self.speedY > 0):
            self.image = image_pirate2
        if (self.speedX < 0):
            self.image = pygame.transform.flip(image_pirate, True, False)
        if (self.speedX > 0):
            self.image = image_pirate

    def keydown(self, key):
        step = 2
        if (key == pygame.K_w):
            self.speedY = -self.scale * step
            self.speedX = 0
        if (key == pygame.K_s):
            self.speedY = self.scale * step
            self.speedX = 0
        if (key == pygame.K_a):
            self.speedX = -self.scale * step
            self.speedY = 0
        if (key == pygame.K_d):
            self.speedX = self.scale * step
            self.speedY = 0

    def keyup(self, key):
        if (key == pygame.K_w):
            if (self.speedY < 0):
                self.speedY = 0
        if (key == pygame.K_s):
            if (self.speedY > 0):
                self.speedY = 0
        if (key == pygame.K_a):
            if (self.speedX < 0):
                self.speedX = 0
        if (key == pygame.K_d):
            if (self.speedX > 0):
                self.speedX = 0


def main():
    global image_cell, image_pirate, image_pirate2, image_pirate3
    pygame.init()
    pygame.display.set_caption('Игра')
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size)
    image_cell = pygame.image.load("cell.png")
    image_pirate = pygame.image.load("pirate.png")
    image_pirate2 = pygame.image.load("pirate2.png")
    image_pirate3 = pygame.image.load("pirate3.png")

    fps = 60
    clock = pygame.time.Clock()
    running = True
    board = Board()
    pirate = Pirate()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_ESCAPE):
                    running = False
                pirate.keyup(event.key)
            if event.type == pygame.KEYDOWN:
                pirate.keydown(event.key)
        pirate.update()
        screen.fill((40, 100, 80))
        board.draw(screen)
        pirate.draw(screen)
        pygame.display.flip()
        print(clock.tick(fps))
    pygame.quit()


if __name__ == '__main__':
    main()
    # a = []
    # b = []
    # for i in range(1, 1920):
    #     if (1920 % i == 0):
    #         a.append(i)
    # for i in range(1, 1080):
    #     if (1080 % i == 0):
    #         b.append(i)
    # c = []
    # for el in a:
    #     if (el in b):
    #         c.append(el)
    # for el in b:
    #     if (el in a and el not in c):
    #         c.append(el)
    # print(" ".join(str(el) for el in a))

# 1 2 3 4 5 6 8 10 12 15 20 24 30 40 60 120
# 1 2 3 4 5 6 8 10 12 15 16 20 24 30 32 40 48 60 64 80 96 120 128 160 192 240 320 384 480 640 960
