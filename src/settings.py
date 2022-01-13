import sys
from ntpath import join


class Settings:
    width = 720 # 1920
    height = 405 # 1080
    fps = 60
    overlay_height = 184
    folder_data = "data"
    folder_saves = "saves"
    folder_images = "images"
    folder_entities = "entities"
    folder_tiles = "tiles"
    folder_worlds = "worlds"
    path_font = None
    screen_width = 15
    screen_height = 7
    demageDelay = 400
    fullscreen = False
    tileSize = 1
    drawHitboxes = True
    drawNoneImgs = False
    moveScreenOnNumpad = True


try:
    # Если программа запущена как exe файл, то данные храняться по такому пути
    newPath = join(sys._MEIPASS, Settings.folder_data)
    Settings.folder_data = newPath
except Exception:
    pass

Settings.tileSize = Settings.width / Settings.screen_width
Settings.overlay_height = Settings.height - Settings.screen_height * Settings.tileSize
Settings.path_font = join(Settings.folder_data, "fonts", "Fifaks10Dev1.ttf")
