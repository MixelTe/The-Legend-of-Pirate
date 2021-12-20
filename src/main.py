import pygame

class Main:
    def __init__(self):
        size = width, height = 600, 600
        self.screen = pygame.display.set_mode(size)

        self.running = True

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((0, 0, 0))
            pygame.display.flip()
            self.screen.fill((0, 0, 0))
        pygame.quit()



if (__name__ == "__main__"):
    Main().start()