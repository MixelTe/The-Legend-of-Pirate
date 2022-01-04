import pygame
from game.entityPlayer import EntityPlayer
from game.overlay import Overlay
from game.screen import Screen
from game.screenAnimation import ScreenAnimation
from game.world import World
from saveData import SaveData
from window import Window
from datetime import datetime

class WindowGame(Window):
    def __init__(self, save: int):
        self.save = save
        self.saveData =  SaveData(save)
        self.player = EntityPlayer(self.saveData)
        self.world: World
        self.screen: Screen
        self.screenAnim: ScreenAnimation = None
        self.overlay = Overlay(self.player)
        self.time = datetime.now()

    def on_event(self, event: pygame.Event):
        # вызывает методы player.keyDown(key), player.keyUp(key), player.onJoyHat(value), player.onJoyButonDown(button), player.onJoyButonUp(button), при соответствующих событиях. Если screenAnim == None.
        # вызывает метод overlay.onClick(pos) при нажатии.
        pass

    def update(self):
        # Если screenAnim не None, то (пропуская пункты ниже) вызывает screenAnim.update(). Если метод возвращает True, то присваеваит None в screenAnim.
        # Вызывает screen.update() если метод возвращает ScreenGoTo, то переключает эран на требуемый: если мир тот же, то создаётся следующий экран и ScreenAnimationMove, если мир другой, то создаётся новый мир, экран и ScreenAnimationBlur. Обновляет информацию в saveData. Присваетвает новый экран в player.screen
        # Вызывает overlay.update(), если метод возвращает True, то вызывает saveData.save() и возвращает WindowStart(mainSurface, save)
        # Проверяет кол-во жизней у игрока. Если их <= 0, то вызывает saveData.save() и возвращает WindowEnd(mainSurface, save)
        pass

    def draw(self, screen: pygame.Surface):
        # Если screenAnim None, то вызывет screen.draw() и выводит полученую картинку на экран, иначе выводит screenAnim.next(). Выводит на экран overlay.draw() и self.screen.draw()
        pass
