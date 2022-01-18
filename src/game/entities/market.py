import pygame
from functions import load_image, load_sound, multPos, renderText, scaleImg
from game.entity import Entity
from settings import Settings

coinImg = scaleImg(load_image("coin.png"), 0.25, 0.3)
font = pygame.font.Font(Settings.path_font, int(Settings.tileSize * 0.4) + 1)
sound_coin = load_sound("coin.wav")


class EntityMarket(Entity):
    def __init__(self, screen, data: dict = None):
        self.item = None
        self.itemId = None
        self.priceImg = None
        self.price = 0
        self.marketId = None
        self.onBuySpeech = "Спасибо за покупку!"
        self.speech = None
        super().__init__(screen, data)
        self.hidden = True
        self.ghostE = True
        self.ghostT = True
        self.drawPriority = 0
        self.width = 1
        self.height = 1
        self.buyZone = (0, 0, 1, 2)
        self.trader = None
        if (self.marketId is not None):
            if (self.marketId in self.screen.saveData.tags):
                self.item = None

    def applyData(self, data: dict):
        super().applyData(data)
        if ("price" in data):
            self.price = data["price"]
        if ("item id" in data):
            self.itemId = data["item id"]
            self.setItem()
        if ("market id" in data):
            id = data["market id"]
            if (id is not None):
                self.marketId = self.screen.world.name + "-market-" + str(id)
        if ("on buy speech" in data):
            speech = data["on buy speech"]
            if (speech is not None):
                self.onBuySpeech = speech
        if ("speech" in data):
            self.speech = data["speech"]

    def setItem(self):
        self.item = Entity.createById(self.itemId, self.screen).image
        self.priceImg = renderText(font, 1, (Settings.tileSize, Settings.tileSize), str(self.price), "black")

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        if (Settings.drawHitboxes):
            self.draw_rect(surface, "pink", self.buyZone, False, True, True)

        if (not self.item):
            return
        itemX = self.x * Settings.tileSize + (self.width * Settings.tileSize - self.item.get_width()) / 2
        itemY = self.y * Settings.tileSize + (self.height * 0.7 * Settings.tileSize - self.item.get_height()) / 2
        surface.blit(self.item, (itemX, itemY))
        surface.blit(coinImg, multPos((self.x, self.y + self.height * 0.7), Settings.tileSize))
        if (self.priceImg):
            surface.blit(self.priceImg, multPos((self.x + 0.3, self.y + self.height * 0.65), Settings.tileSize))

    def update(self):
        super().update()
        if (self.trader is None):
            for e in self.screen.entities:
                if (e.id == "trader"):
                    self.trader = e
                    break
        if (self.item and self.is_inRectD(self.buyZone, self.screen.player)):
            self.screen.player.action = self.buy
            if (self.trader and self.speech is not None):
                self.trader.setSpeech(self.speech)

    def buy(self):
        if (self.screen.saveData.coins >= self.price):
            self.trader.somethingBought(self.onBuySpeech)
            sound_coin.play()
            if (self.marketId is not None):
                self.screen.saveData.tags.append(self.marketId)
            self.screen.saveData.coins -= self.price
            if (self.itemId == "coin"):
                self.screen.saveData.coins += 1
            elif (self.itemId == "heart"):
                self.screen.player.heal(1)
            self.item = None


Entity.registerEntity("market", EntityMarket)
