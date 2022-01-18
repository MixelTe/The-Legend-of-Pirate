import pygame
from functions import getPosMult, getRectMult, load_image, load_sound, renderText
from game.entityPlayer import EntityPlayer
from game.dialogs.exit import GameDialog_exit
from settings import Settings


multRect = getRectMult(Settings.width, Settings.overlay_height)
multPos = getPosMult(Settings.width, Settings.overlay_height)

heartSize = Settings.tileSize * 0.8
img_heart = pygame.transform.scale(load_image("hpF.png"), (heartSize, heartSize))
img_heartHalf = pygame.transform.scale(load_image("hp.png"), (heartSize, heartSize))
img_heartEmpty = pygame.transform.scale(load_image("hpE.png"), (heartSize, heartSize))
img_coin = pygame.transform.scale(load_image("coin.png"), (Settings.tileSize * 0.333, Settings.tileSize * 0.4))
exitBtn = multRect((0.8, 0.15, 0.18, 0.7))
img_exitBtn = pygame.transform.scale(load_image("quit.png"), (exitBtn[2], exitBtn[3]))
img_exitBtn_active = pygame.transform.scale(load_image("quit_active.png"), (exitBtn[2], exitBtn[3]))
img_msgBox = pygame.transform.scale(load_image("msgBox.png"), multPos((0.5, 1)))

sound_btn = load_sound("btn.mp3")
sound_btn2 = load_sound("btn2.wav")


class Overlay:
    def __init__(self, player: EntityPlayer):
        self.surface = pygame.Surface((Settings.width, Settings.overlay_height))
        self.player = player
        self.exit = False

        self.exitBtn = exitBtn
        self.exitBtn_hover = False

        self.msgBox = multRect((0.25, 0, 0.5, 1))
        self.msgBox_text = multRect((0.27, 0.07, 0.48, 0.95))
        self.text_past = ""
        self.text_img = None

        self.fontM = pygame.font.Font(Settings.path_font, int(Settings.tileSize * 0.4) + 1)
        self.fontL = pygame.font.Font(Settings.path_font, int(Settings.tileSize * 0.55) + 1)

        self.heartsPos = multPos((0.03, 0.35))
        self.coinPos = multPos((0.02, 0.08))
        self.coinText = multRect((0.05, 0.05, 0.48, 0.9))
        self.text_coin_past = -1
        self.text_coin = None

    def update(self) -> bool:
        if (self.text_past != self.player.message):
            self.text_past = self.player.message
            self.text_img = renderText(self.fontM, int(Settings.tileSize * 0.27) + 1,
                                       self.msgBox_text.size, self.player.message, pygame.Color(81, 44, 40))
        if (self.text_coin_past != self.player.saveData.coins):
            self.text_coin_past = self.player.saveData.coins
            self.text_coin = renderText(self.fontL, int(Settings.tileSize * 0.44) + 1,
                                        self.msgBox_text.size, str(self.text_coin_past), "black")
        return self.exit

    def draw(self) -> pygame.Surface:
        self.surface.fill("#00ADAD")
        if (self.exitBtn_hover):
            self.surface.blit(img_exitBtn_active, (exitBtn[0], exitBtn[1]))
        else:
            self.surface.blit(img_exitBtn, (exitBtn[0], exitBtn[1]))

        # pygame.draw.rect(self.surface, pygame.Color(194, 133, 105), self.msgBox, 0, int(Settings.tileSize * 0.2))
        self.surface.blit(img_msgBox, self.msgBox.topleft)
        if (self.text_img is not None):
            self.surface.blit(self.text_img, self.msgBox_text.topleft)

        for i in range(3):
            pos = (self.heartsPos[0] + (heartSize + Settings.tileSize * 0.2) * i, self.heartsPos[1])
            if (self.player.health >= (i + 1) * 2):
                self.surface.blit(img_heart, pos)
            elif (self.player.health >= (i + 1) * 2 - 1):
                self.surface.blit(img_heartHalf, pos)
            else:
                self.surface.blit(img_heartEmpty, pos)

        self.surface.blit(img_coin, self.coinPos)
        if (self.text_coin):
            self.surface.blit(self.text_coin, self.coinText.topleft)

        return self.surface

    def openDialog(self):
        sound_btn.play()
        def onClose(r: bool):
            self.exit = r
        self.exitBtn_hover = False
        self.player.screen.openDialog(GameDialog_exit(onClose))

    def onClick(self, pos: tuple[int, int]):
        if (self.exitBtn.collidepoint(pos)):
            self.openDialog()

    def onMouseMove(self, pos: tuple[int, int]):
        hover = self.exitBtn.collidepoint(pos)
        if (hover and not self.exitBtn_hover):
            sound_btn2.play()
        self.exitBtn_hover = hover

    def onKeyUp(self, key):
        if (key == pygame.K_ESCAPE):
            self.openDialog()

    def onJoyButonUp(self, button):
        if (button == 6):
            self.openDialog()
