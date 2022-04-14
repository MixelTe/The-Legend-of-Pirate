import pygame
from backMusic import endBattleMusic
from functions import calcPlayerCoinsAfterDeath, load_sound
from game.dialogs.start import GameDialog_start
from game.entityPlayer import EntityPlayer
from game.gameDialog import GameDialog
from game.overlay import Overlay
from game.screen import Screen
from game.screenAnimation import ScreenAnimation, ScreenAnimationBlur, ScreenAnimationDeath, ScreenAnimationMove
from game.world import World
from game.saveData import SaveData
from settings import Settings
from window import Window
from datetime import datetime

sound_over = load_sound("gameover.mp3")


class WindowGame(Window):
    def __init__(self, save: int):
        self.save = save
        self.saveData = SaveData(save).load()
        self.player = EntityPlayer(self.saveData)
        self.world = World.getWorld(self.saveData.world)
        self.screen: Screen = Screen.create(self.world, *self.saveData.screen, self.saveData, self.player, self.openDialog)
        self.screenAnim: ScreenAnimation = None
        self.overlay = Overlay(self.player)
        self.dialog: GameDialog = None
        self.time = datetime.now()
        if (self.saveData.time == 0):
            self.dialog = GameDialog_start()

    def on_event(self, event: pygame.event.Event):
        if (Settings.deathMouse):
            if (event.type == pygame.MOUSEBUTTONUP):
                self.deathMouse(event.pos)
        if (self.dialog is None):
            if (event.type == pygame.KEYDOWN):
                self.player.onKeyDown(event.key)
            if (event.type == pygame.KEYUP):
                self.player.onKeyUp(event.key)
            if (event.type == pygame.JOYBUTTONDOWN):
                self.player.onJoyButonDown(event.button)
            if (event.type == pygame.JOYBUTTONUP):
                self.player.onJoyButonUp(event.button)
            if (event.type == pygame.JOYHATMOTION):
                self.player.onJoyHat(event.value)
            if (event.type == pygame.JOYAXISMOTION):
                self.player.onJoyAxis(event.axis, event.value)
            if (event.type == pygame.MOUSEBUTTONUP):
                self.overlay.onClick(event.pos)
            if (event.type == pygame.MOUSEMOTION):
                self.overlay.onMouseMove(event.pos)
            if (event.type == pygame.JOYBUTTONUP):
                self.overlay.onJoyButonUp(event.button)
            if (event.type == pygame.KEYUP):
                self.overlay.onKeyUp(event.key)
        else:
            if (event.type == pygame.MOUSEMOTION):
                self.dialog.onMove(event.pos)
            if (event.type == pygame.MOUSEBUTTONUP):
                self.dialog.onMouseUp(event.pos)
            if (event.type == pygame.KEYUP):
                self.dialog.onKeyUp(event.key)
            if (event.type == pygame.JOYBUTTONUP):
                self.dialog.onJoyButonUp(event.button)
            if (event.type == pygame.JOYHATMOTION):
                self.dialog.onJoyHat(event.value)
            if (event.type == pygame.JOYAXISMOTION):
                self.dialog.onJoyAxis(event.axis, event.value)

    def update(self):
        exitNow = self.overlay.update()
        if (exitNow):
            self.saveAll()
            from windowStart import WindowStart
            return WindowStart()

        if (self.dialog is not None):
            r = self.dialog.update()
            if (r):
                if (self.dialog.exitFromGame):
                    self.saveAll()
                    from windowStart import WindowStart
                    return WindowStart()
                self.dialog = None
            return
        if (self.screenAnim):
            done = self.screenAnim.update()
            if (done):
                if (isinstance(self.screenAnim, ScreenAnimationDeath)):
                    from windowEnd import WindowEnd
                    return WindowEnd(self.save, self.player.lastAttaker)
                self.screenAnim = None
            return
        goTo = self.screen.update()
        if (goTo):
            if (goTo.world == self.world.name):
                dx = 0
                dy = 0
                if (goTo.screen[0] > self.screen.pos[0]):
                    dx = 1
                elif (goTo.screen[0] < self.screen.pos[0]):
                    dx = -1
                if (goTo.screen[1] > self.screen.pos[1]):
                    dy = 1
                elif (goTo.screen[1] < self.screen.pos[1]):
                    dy = -1
                if (goTo.pos):
                    self.player.centerTo(goTo.pos)
                self.screen = Screen.create(self.world, *goTo.screen, self.saveData, self.player, self.openDialog)
                self.screen.update()
                self.screenAnim = ScreenAnimationMove(goTo.image, self.screen.draw(), (dx, dy))
            else:
                if (goTo.pos):
                    self.player.centerTo(goTo.pos)
                self.world = World.getWorld(goTo.world)
                self.screen = Screen.create(self.world, *goTo.screen, self.saveData, self.player, self.openDialog)
                self.screen.update()
                self.screenAnim = ScreenAnimationBlur(goTo.image, self.screen.draw())

        if (self.player.health <= 0):
            coins = self.saveData.coins
            self.saveData.coins = calcPlayerCoinsAfterDeath(self.saveData.tags, self.saveData.coins)
            self.saveAll()
            self.saveData.coins = coins
            endBattleMusic()
            self.player.death()
            sound_over.play()
            self.screenAnim = ScreenAnimationDeath(self.screen.draw(False), self.player)

    def draw(self, screen: pygame.Surface):
        if (self.screenAnim):
            screenImg = self.screenAnim.draw()
        else:
            screenImg = self.screen.draw()
        overlay = self.overlay.draw()
        screen.blit(overlay, (0, 0))
        screen.blit(screenImg, (0, Settings.overlay_height))
        if (self.dialog is not None):
            screen.blit(self.dialog.draw(), self.dialog.rect.topleft)

    def openDialog(self, dialog: GameDialog):
        self.dialog = dialog

    def saveAll(self):
        self.saveData.health = self.player.health
        if (self.player.health <= 0):
            self.saveData.health = SaveData(-1).health
        now = datetime.now()
        self.saveData.time += int((now - self.time).total_seconds())
        self.time = now
        self.saveData.save()

    def deathMouse(self, pos: tuple[int, int]):
        pos = list(pos)
        pos[1] -= Settings.overlay_height
        pos = (pos[0] / Settings.tileSize, pos[1] / Settings.tileSize)
        self.screen.deathMouse(pos)
