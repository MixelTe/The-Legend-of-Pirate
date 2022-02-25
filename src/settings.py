import sys
from os.path import join


class Settings:
    version = "v2.0.0 (dev)"
    width = 720  # 1920
    height = 405  # 1080
    fps = 60
    overlay_height = 184
    folder_data = "data"
    folder_saves = "saves"
    folder_images = "images"
    folder_entities = "entities"
    folder_decor = "decor"
    folder_tiles = "tiles"
    folder_worlds = "worlds"
    folder_sounds = "sounds"
    path_font = None
    screen_width = 20
    screen_height = 9
    damageDelay = 400
    damageDelayPlayer = 1600
    fullscreen = False
    tileSize = 1
    drawHitboxes = False
    drawNoneImgs = False
    drawGrid = False
    disableAI = False
    ghostmode = True
    moveScreenOnNumpad = True


try:
    # Если программа запущена как exe файл, то данные храняться по такому пути
    newPath = join(sys._MEIPASS, Settings.folder_data)
    Settings.folder_data = newPath
except Exception:
    pass

Settings.tileSize = Settings.width // Settings.screen_width
Settings.overlay_height = Settings.height - Settings.screen_height * Settings.tileSize
Settings.path_font = join(Settings.folder_data, "fonts", "Fifaks10Dev1.ttf")
