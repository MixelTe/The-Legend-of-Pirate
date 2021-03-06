import sys
from os.path import join, expanduser


class Settings:
    version = "v2.0.1"
    width = 720  # 1920
    height = 405  # 1080
    windowed = False
    fps = 60
    overlay_height = 184
    folder_data = "data"
    folder_saves = "The Legend of Pirate - Saves"
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
    fullscreen = True
    tileSize = 1
    DEVMode = False
    drawHitboxes = False  # F1
    disableAI = False  # F4
    ghostmode = False  # F5
    drawGrid = False  # F6
    deathMouse = False  # F7
    drawNoneImgs = False
    moveScreenOnNumpad = False


try:
    # Если программа запущена как exe файл, то данные храняться по такому пути
    newPath = join(sys._MEIPASS, Settings.folder_data)
    Settings.folder_data = newPath
except Exception:
    pass

Settings.path_font = join(Settings.folder_data, "fonts", "Fifaks10Dev1.ttf")
if (Settings.windowed):
    Settings.fullscreen = False


try:
    import ctypes.wintypes
    CSIDL_PERSONAL = 5
    SHGFP_TYPE_CURRENT = 0
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)
    path = join(buf.value, Settings.folder_saves)
    Settings.folder_saves = path
except:
    Settings.folder_saves = join(expanduser('~'), "Documents", Settings.folder_saves)


def setSizes(desktop_size):
    if (not Settings.windowed):
        Settings.width = desktop_size[0]
        Settings.height = Settings.width / 16 * 9
        if (Settings.height > desktop_size[1]):
            Settings.height = desktop_size[1]
            Settings.width = Settings.height / 9 * 16

    Settings.tileSize = Settings.width // Settings.screen_width
    Settings.overlay_height = Settings.height - Settings.screen_height * Settings.tileSize
