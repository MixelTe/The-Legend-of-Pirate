import pygame
from game.entityPlayer import EntityPlayer
from game.gameDialog import GameDialog
from game.overlay import Overlay
from game.screen import Screen
from game.screenAnimation import ScreenAnimation, ScreenAnimationBlur, ScreenAnimationMove
from game.world import World
from game.saveData import SaveData
from settings import Settings
from window import Window
from datetime import datetime


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

    def on_event(self, event: pygame.event.Event):
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
        else:
            if (event.type == pygame.MOUSEMOTION):
                self.dialog.onMove(event.pos)
            if (event.type == pygame.MOUSEBUTTONUP):
                self.dialog.onMouseUp(event.pos)
            if (event.type == pygame.KEYUP):
                self.dialog.onKeyUp(event.key)
            if (event.type == pygame.JOYBUTTONDOWN):
                self.dialog.onJoyButonUp(event.button)
            if (event.type == pygame.JOYHATMOTION):
                self.dialog.onJoyHat(event.value)
            if (event.type == pygame.JOYAXISMOTION):
                self.dialog.onJoyAxis(event.axis, event.value)

    def update(self):
        exitNow = self.overlay.update()
        if (exitNow):
            self.saveData.health = self.player.health
            self.saveData.time += int((datetime.now() - self.time).total_seconds())
            self.saveData.save()
            from windowStart import WindowStart
            return WindowStart()

        if (self.dialog is not None):
            r = self.dialog.update()
            if (r):
                self.dialog = None
            return
        if (self.screenAnim):
            done = self.screenAnim.update()
            if (done):
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
                self.screen = Screen.create(self.world, *goTo.screen, self.saveData, self.player, self.openDialog)
                self.screenAnim = ScreenAnimationMove(goTo.image, self.screen.draw(), (dx, dy))
            else:
                self.world = World.getWorld(goTo.world)
                self.screen = Screen.create(self.world, *goTo.screen, self.saveData, self.player, self.openDialog)
                self.screenAnim = ScreenAnimationBlur(goTo.image, self.screen.draw())

        if (self.player.health <= 0):
            self.saveData.health = SaveData(-1).health
            self.saveData.time += int((datetime.now() - self.time).total_seconds())
            self.saveData.save()
            from windowEnd import WindowEnd
            return WindowEnd(self.save)

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
