try:
    import main
except:
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, "Произошла ошибка", "The Legend of Pirate", 0x10)
    except:
        pass
