import pygame
from game.entityPlayer import EntityPlayer
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
        self.screen: Screen = Screen.create(self.world, *self.saveData.screen, self.saveData, self.player)
        self.screenAnim: ScreenAnimation = None
        self.overlay = Overlay(self.player)
        self.time = datetime.now()

    def on_event(self, event: pygame.event.Event):
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

    def update(self):
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
                self.screen = Screen.create(self.world, *goTo.screen, self.saveData, self.player)
                self.screenAnim = ScreenAnimationMove(goTo.image, self.screen.draw(), (dx, dy))
            else:
                self.world = World.getWorld(goTo.world)
                self.screen = Screen.create(self.world, *goTo.screen, self.saveData, self.player)
                self.screenAnim = ScreenAnimationBlur(goTo.image, self.screen.draw())
        exitNow = self.overlay.update()
        if (exitNow):
            self.saveData.save()
            from windowStart import WindowStart
            return WindowStart()
        if (self.player.health <= 0):
            self.saveData.health = SaveData(0).health
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
