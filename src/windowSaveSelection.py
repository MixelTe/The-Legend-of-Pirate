import pygame
from game.saveData import SaveData
from settings import Settings
from window import WindowWithButtons
from functions import Button, createButton, getGameProgress, load_image
from windowGame import WindowGame

heartSize = int(Settings.tileSize * 0.9)
img_heart = pygame.transform.scale(load_image("hpA.png"), (heartSize, heartSize))
img_coin = pygame.transform.scale(load_image("coin.png"), (int(Settings.tileSize * 0.6), int(Settings.tileSize * 0.72)))
font = pygame.font.Font(Settings.path_font, int(Settings.tileSize * 1) + 1)


class WindowSaveSelection(WindowWithButtons):
    def __init__(self):
        super().__init__()
        self.all_sprites = pygame.sprite.Group()
        self.dialog = None
        self.toStartWindow = False
        scale = 0.38

        self.btns = {
            0: createSaveButton(1, scale, self.all_sprites, 0.3, 0.03),
            1: createSaveButton(2, scale, self.all_sprites, 0.3, 0.36),
            2: createSaveButton(3, scale, self.all_sprites, 0.3, 0.68),
        }

        scale = 0.4 / 25 * 9
        self.btn_delete = {0: None, 1: None, 2: None}
        if (SaveData.exist(1)):
            self.btn_delete[0] = createButton("cross", scale, self.all_sprites, 0.72, 0.05)
        if (SaveData.exist(2)):
            self.btn_delete[1] = createButton("cross", scale, self.all_sprites, 0.72, 0.37)
        if (SaveData.exist(3)):
            self.btn_delete[2] = createButton("cross", scale, self.all_sprites, 0.72, 0.7)

        self.btn_back = createButton("back", 0.1, self.all_sprites, 0.03, 0.78)

        self.startSave = None

    def action(self):
        if (0 <= self.selected < 3):
            self.startSave = self.selected + 1
        if (3 <= self.selected):
            btn = self.all_sprites.sprites()[self.selected]
            if (btn == self.btn_delete[0]):
                self.selected = 0
            elif (btn == self.btn_delete[1]):
                self.selected = 1
            elif (btn == self.btn_delete[2]):
                self.selected = 2
            elif (btn == self.btn_back):
                self.toStartWindow = True
                return
            else:
                return
            super().update()
            self.dialog = DialogDelete(self.selected, self.onDialogClose)

    def onDialogClose(self, v):
        if (v):
            SaveData.delete(self.dialog.save + 1)
            if (self.dialog.save in self.btn_delete):
                btn = self.btn_delete[self.dialog.save]
                self.btn_delete[self.dialog.save] = None
                self.all_sprites.remove(btn)
                btnS = self.btns[self.dialog.save]
                btnS.img = btnS.img_new
                btnS.img_a = btnS.img_new_a
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
        if (self.toStartWindow):
            from windowStart import WindowStart
            return WindowStart()
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


def createSaveButton(save, scale, group, x, y):
    exist = SaveData.exist(save)
    img_new = load_image(f"save_new{save}.png")
    img_new_a = load_image(f"save_new{save}_active.png")
    if (exist):
        img = load_image(f"save{save}.png")
        img_a = load_image(f"save{save}_active.png")
    else:
        img = img_new
        img_a = img_new_a
    scale = Settings.width * scale / img.get_width()
    w, h = int(img.get_width() * scale), int(img.get_height() * scale)
    img = pygame.transform.scale(img, (w, h))
    img_a = pygame.transform.scale(img_a, (w, h))
    wn, hn = int(img_new.get_width() * scale), int(img_new.get_height() * scale)
    img_new = pygame.transform.scale(img_new, (wn, hn))
    img_new_a = pygame.transform.scale(img_new_a, (wn, hn))
    if (exist):
        saveData = SaveData(save).load()
        coins = font.render(F"{saveData.coins}", True, pygame.Color(81, 44, 40))
        coinPos = (int(w * 0.07), int(h * 0.68))
        coinsPos = (int(w * 0.17), int(h * 0.65))
        img.blit(img_coin, coinPos)
        img.blit(coins, coinsPos)
        img_a.blit(img_coin, coinPos)
        img_a.blit(coins, coinsPos)
        progress = font.render(F"{getGameProgress(saveData.tags)}%", True, "#FFD700")
        progressPos = ((w - progress.get_width()) - int(w * 0.05), int(h * 0.65))
        img.blit(progress, progressPos)
        img_a.blit(progress, progressPos)
        if ("heart-collected" in saveData.tags):
            heartPos = (int(w * 0.5), int(h * 0.65))
            img.blit(img_heart, heartPos)
            img_a.blit(img_heart, heartPos)
    sprite = Button(group, img, img_a)
    sprite.img_new = img_new
    sprite.img_new_a = img_new_a
    sprite.rect = pygame.Rect(x * Settings.width, y * Settings.height, w,  h)
    return sprite
