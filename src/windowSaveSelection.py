import pygame
from game.saveData import SaveData
from settings import Settings
from window import WindowWithButtons
from functions import createButton
from windowGame import WindowGame


class WindowSaveSelection(WindowWithButtons):
    def __init__(self):
        super().__init__()
        self.all_sprites = pygame.sprite.Group()
        self.dialog = None
        scale = 0.4

        createButton("save1", scale, self.all_sprites, 0.3, 0.05)
        createButton("save2", scale, self.all_sprites, 0.3, 0.37)
        createButton("save3", scale, self.all_sprites, 0.3, 0.7)

        scale = 0.4 / 25 * 9
        self.btn_delete = {}
        if (SaveData.exist(1)):
            self.btn_delete[0] = createButton("cross", scale, self.all_sprites, 0.72, 0.05)
        if (SaveData.exist(2)):
            self.btn_delete[1] = createButton("cross", scale, self.all_sprites, 0.72, 0.37)
        if (SaveData.exist(3)):
            self.btn_delete[2] = createButton("cross", scale, self.all_sprites, 0.72, 0.7)

        self.startSave = None

    def action(self):
        if (0 <= self.selected < 3):
            self.startSave = self.selected + 1
        if (3 <= self.selected):
            self.selected -= 3
            super().update()
            self.dialog = DialogDelete(self.selected, self.onDialogClose)

    def onDialogClose(self, v):
        if (v):
            SaveData.delete(self.dialog.save + 1)
            if (self.dialog.save in self.btn_delete):
                btn = self.btn_delete[self.dialog.save]
                self.btn_delete[self.dialog.save] = None
                self.all_sprites.remove(btn)
        self.dialog = None

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        if (self.dialog):
            self.dialog.draw(screen)

    def on_event(self, event: pygame.event.Event):
        if (self.dialog):
            self.dialog.on_event(event)
        else:
            super().on_event(event)

    def update(self):
        if (self.dialog):
            self.dialog.update()
        else:
            super().update()
            if (self.startSave is not None):
                return WindowGame(self.startSave)


class DialogDelete(WindowWithButtons):
    def __init__(self, save, onClose):
        super().__init__()
        self.all_sprites = pygame.sprite.Group()
        self.onClose = onClose
        self.save = save
        self.rect = [0, 0, Settings.width * 0.65, Settings.height * 0.5]
        self.rect[0] = (Settings.width - self.rect[2]) // 2
        self.rect[1] = (Settings.height - self.rect[3]) // 2
        self.textPos = (self.rect[0] + Settings.width * 0.035, self.rect[1] + Settings.height * 0.05)
        scale = 0.2

        font = pygame.font.Font(Settings.path_font, int(Settings.width * 0.06) + 1)
        self.text = font.render("Удалить сохранение?", True, pygame.Color(81, 44, 40))
        createButton("yes", scale, self.all_sprites, 0.26, 0.44)
        createButton("no", scale, self.all_sprites, 0.54, 0.44)

        self.back = pygame.Surface((self.rect[2], self.rect[3]))
        self.back.fill(pygame.Color(228, 164, 128))
        pygame.draw.rect(self.back, pygame.Color(194, 133, 105),
                         (0, 0, self.rect[2], self.rect[3]), int(Settings.width * 0.05) + 1)

        self.selected = 1

    def action(self):
        if (self.selected == 0):
            self.onClose(True)
        if (self.selected == 1):
            self.onClose(False)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.back, (self.rect[0], self.rect[1]))
        screen.blit(self.text, self.textPos)
        self.all_sprites.draw(screen)
