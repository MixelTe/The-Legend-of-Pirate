import pygame
from functions import getPosMult, getRectMult, joinPath, load_image, load_sound, renderText
from game.entityPlayer import EntityPlayer
from game.dialogs.exit import GameDialog_exit
from settings import Settings


multRect = getRectMult(Settings.width, Settings.overlay_height)
multPos = getPosMult(Settings.width, Settings.overlay_height)

heartSize = int(Settings.tileSize * 1.06)
img_heart = pygame.transform.scale(load_image("hpF.png"), (heartSize, heartSize))
img_heartHalf = pygame.transform.scale(load_image("hp.png"), (heartSize, heartSize))
img_heartEmpty = pygame.transform.scale(load_image("hpE.png"), (heartSize, heartSize))
img_coin = pygame.transform.scale(load_image("coin.png"), (int(Settings.tileSize * 0.444), int(Settings.tileSize * 0.533)))
exitBtn = multRect((0.8, 0.19, 0.18, 0.62))
img_exitBtn = pygame.transform.scale(load_image("quit.png"), (int(exitBtn[2]), int(exitBtn[3])))
img_exitBtn_active = pygame.transform.scale(load_image("quit_active.png"), (int(exitBtn[2]), int(exitBtn[3])))
img_msgBox = pygame.transform.scale(load_image("msgBox.png"), (int(0.5 * Settings.width), int(1 * Settings.overlay_height)))
img_map1 = pygame.transform.scale(load_image("map1.png"), (int(Settings.tileSize * 1.03), int(Settings.tileSize * 0.56)))
img_map2 = pygame.transform.scale(load_image("map2.png"), (int(Settings.tileSize * 1.03), int(Settings.tileSize * 0.56)))
img_spyglass = pygame.transform.scale(load_image(joinPath(Settings.folder_entities, "spyglass.png")), (int(Settings.tileSize * 1.237), int(Settings.tileSize * 0.45)))
img_iconE = pygame.transform.scale(load_image("E.png"), (int(Settings.tileSize * 0.7), int(Settings.tileSize * 0.7)))
img_iconB = pygame.transform.scale(load_image("B.png"), (int(Settings.tileSize * 0.7), int(Settings.tileSize * 0.7)))
img_coinbag = pygame.transform.scale(load_image("coinbag.png"), (int(Settings.tileSize * 0.75), int(Settings.tileSize * 0.6)))

sound_btn = load_sound("btn1.mp3", "btn")
sound_btn2 = load_sound("btn2.wav", "btn")


class Overlay:
    def __init__(self, player: EntityPlayer):
        self.surface = pygame.Surface((Settings.width, Settings.overlay_height))
        self.player = player
        self.exit = False

        self.exitBtn = exitBtn
        self.exitBtn_hover = False

        self.msgBox = multRect((0.25, 0, 0.5, 1))
        self.msgBox_text = multRect((0.268, 0.07, 0.467, 0.87))
        self.text_past = ""
        self.text_img = None

        self.fontM = pygame.font.Font(Settings.path_font, int(Settings.tileSize * 0.53) + 1)
        self.fontL = pygame.font.Font(Settings.path_font, int(Settings.tileSize * 0.73) + 1)

        self.heartsPos = multPos((0.025, 0.5))
        self.heartsFourPos = multPos((0.012, 0.5))
        self.coinPos = multPos((0.016, 0.16))
        self.coinText = multRect((0.045, 0.13, 0.48, 0.9))
        self.map1Pos = multPos((0.195, 0.03))
        self.map2Pos = multPos((0.195, 0.27))
        self.spyglassPos = multPos((0.125, 0.18))
        self.coinbagPos = multPos((0.756, 0.06))
        self.text_coin_past = -1
        self.text_coin = None

        self.iconPos = multPos((0.73, 0.7))
        self.iconCounter = -1

    def update(self) -> bool:
        if (self.text_past != self.player.message):
            self.text_past = self.player.message
            self.text_img = renderText(self.fontM, int(Settings.tileSize * 0.35) + 1,
                                       self.msgBox_text.size, self.player.message, pygame.Color(81, 44, 40))
        if (self.text_coin_past != self.player.saveData.coins):
            self.text_coin_past = self.player.saveData.coins
            self.text_coin = renderText(self.fontL, int(Settings.tileSize * 0.54) + 1,
                                        self.msgBox_text.size, str(self.text_coin_past), "black")
        if (self.player.messageIsLong):
            self.iconCounter += 1000 / Settings.fps
            self.iconCounter = self.iconCounter % 1600
        else:
            self.iconCounter = -1
        return self.exit

    def draw(self) -> pygame.Surface:
        self.surface.fill("#00ADAD")
        if (self.exitBtn_hover):
            self.surface.blit(img_exitBtn_active, (exitBtn[0], exitBtn[1]))
        else:
            self.surface.blit(img_exitBtn, (exitBtn[0], exitBtn[1]))

        # pygame.draw.rect(self.surface, pygame.Color(194, 133, 105), self.msgBox, 0, int(Settings.tileSize * 0.2))
        self.surface.blit(img_msgBox, self.msgBox.topleft)
        # pygame.draw.rect(self.surface, pygame.Color(194, 133, 0), self.msgBox_text)
        if (self.text_img is not None):
            self.surface.blit(self.text_img, self.msgBox_text.topleft)

        fourHearts = "heart-collected" in self.player.saveData.tags
        for i in range(4 if fourHearts else 3):
            if (fourHearts):
                pos = (self.heartsFourPos[0] + (heartSize + Settings.tileSize * 0.1) * i, self.heartsFourPos[1])
            else:
                pos = (self.heartsPos[0] + (heartSize + Settings.tileSize * 0.4) * i, self.heartsPos[1])
            if (self.player.health >= (i + 1) * 2):
                self.surface.blit(img_heart, pos)
            elif (self.player.health >= (i + 1) * 2 - 1):
                self.surface.blit(img_heartHalf, pos)
            else:
                self.surface.blit(img_heartEmpty, pos)

        self.surface.blit(img_coin, self.coinPos)
        if (self.text_coin):
            self.surface.blit(self.text_coin, self.coinText.topleft)

        if ("quest-pirate-ended" in self.player.saveData.tags or "quest-cactus-ended" in self.player.saveData.tags):
            self.surface.blit(img_map1, self.map1Pos)
        if ("quest-pirate-ended" in self.player.saveData.tags and "quest-cactus-ended" in self.player.saveData.tags):
            self.surface.blit(img_map2, self.map2Pos)
        if ("quest-pirate-tubeFound" in self.player.saveData.tags and "quest-pirate-ended" not in self.player.saveData.tags):
            self.surface.blit(img_spyglass, self.spyglassPos)

        coinbagCount = 0
        coinbagCount += 1 if "coinbag-1" in self.player.saveData.tags else 0
        coinbagCount += 1 if "coinbag-2" in self.player.saveData.tags else 0
        coinbagCount += 1 if "coinbag-3" in self.player.saveData.tags else 0
        for i in range(coinbagCount):
            pos = (self.coinbagPos[0], self.coinbagPos[1] + Settings.tileSize * 0.7 * i)
            self.surface.blit(img_coinbag, pos)

        if (self.iconCounter > -1):
            iconImg = img_iconE if self.player.keyboardIsUsed else img_iconB
            if (self.iconCounter < 1000):
                self.surface.blit(iconImg, self.iconPos)
            else:
                size = iconImg.get_size()
                s = 0.8
                sizeN = (size[0] * s, size[1] * s)
                img = pygame.transform.scale(iconImg, sizeN)
                pos = (self.iconPos[0] + (size[0] - sizeN[0]) / 2, self.iconPos[1] + (size[1] - sizeN[1]) / 2)
                self.surface.blit(img, pos)

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
