1. Класс Main
	* Создаётся на старте программы и вызывается метод start
	* Поля:
		* screen: Surface - Главный холст
		* window: Window - Текущее окно. При старте: WindowStart
	* Методы:
		1. init() - создание окна 1920x1080 в полноэкранном режиме
		2. start() - запуск игрового цикла. Цикл вызывает методы on_event, calc и draw у window. Если функция calc возвращает Window, то текущее окно заменяется на него.
---
2. Класс Settings
	* Содержит все системные настройки игры
	* Поля:
		* width = 1920
		* height = 1080
		* heightOverlay: int
		* folder_data = "data"
		* folder_save = "save"
		* folder_images = "images"
---
3. Класс Window
	* Базовый класс окна
	* Поля:
		* mainSurface: pygame.Surface
	* Методы:
		1. init(mainSurface: pygame.Surface)
		2. on_event(event: Event) - обрабатывает событие
		3. calc() -> None | Window - просчитывает новый кадр
		4. draw(screen: Surface) - рисует текущий кадр
---
4. Класс WindowStart(Window)
	* Стартовое окно.
	* Поля:
		* save: int - ячейка сохранения
	* Методы:
		1. init(mainSurface: pygame.Surface, save: int = 1)
	* Кнопки:
		2. "Старт" - запуск игры, при нажатии метод calc возвращает WindowGame(mainSurface, save)
		3. "Статистика" - при нажатии метод calc возвращает WindowStatistics(mainSurface, save)
		4. Выбор ячейки сохранения - три кнопки: "1", "2" и "3". При нажатии на кнопки save меняется на соответствующее значение.
		5. "Выйти" - при нажатии создаёт событие quit.
		```python
		pygame.event.post(pygame.event.Event(pygame.QUIT))
		```
---
5. Класс WindowStatistics(Window)
	* Отображает статистику текущего сохранения
	* Поля:
		* save: int - ячейка сохранения
	* Методы:
		1. init(mainSurface: pygame.Surface, save: int)
	* Кнопки:
		2. "Назад" - при нажатии метод calc возвращает WindowStart(mainSurface, save)
---
6. Класс WindowEnd(Window)
	* Финальный экран. Возможно титры или просто благодарность за игру. Включается после победы над боссом. После показа титров или нажатия кнопки "Продолжить" метод calc возвращает WindowStatistics(mainSurface, save)
	* Поля:
		* save: int - ячейка сохранения
	* Методы:
		1. init(mainSurface: pygame.Surface, save: int)
---
7. Класс WindowGame(Window)
	* Игровой движок
	* Поля:
		* save: int - ячейка сохранения
		* saveData: SaveData
		* player: SptitePlayer
		* world: World
		* screen: Screen
		* screenMove: ScreenMove | None
		* overlay: Overlay
	* Методы:
		1. init(mainSurface: pygame.Surface, save: int) - загрузка сохранения и создание текущего мира и экрана
		2. on_event(event: Event) - вызывает методы player.keyDown(key) и player.keyUp(key), при соответствующих событиях
		3. calc() -> None | Window
			* Вызывает screen.calc(player) если метод возвращает ScreenGoTo, то переключает эран на требуемый: если мир тот же, то создаётся следующий экран и ScreenMove, если мир другой, то создаётся новый мир и экран. Обновляет информацию в saveData
			* Вызывает overlay.calc(), если метод возвращает True, то вызывает saveData.save() и возвращает WindowStart(mainSurface, save)
		4. draw() - Если screenMove None, то вызывет screen.draw() и выводит полученую картинку на экран, иначе выводит screenMove.next(). Выводит на экран overlay.draw()
---
8. Класс SaveData
	* Все данные, необходимые для сохранения прогресса игрока
	* Поля:
		* save: int - ячейка сохранения
		* saveVersion: int - версия файла сохранения
		* playerX: float
		* playerY: float
		* world: str - мир в котором находится игрок
		* screen: tuple[int, int] - экран на котором находится игрок
		* coins: int
		* health: int
		* tags: list\[str] - тэги. Например: "дверь1 открыта"
	* Методы:
		1. init(save: int)
		2. load() - если файла сохранения нет, то оставляет значения по умолчанию
		3. save()
	* Формат сохранения:
		* Строка, которая начинается с //, пропускается при считывании данных
		```
		// координаты
		playerX playerY
		world
		screen[0] screen[1]
		// состояние игрока
		coins
		health
		// тэги, в одну строку, через точку с запятой (;)
		";".join(tags)
		```
---
9. Класс Screen
	> В разработке
	* Логика и отрисовка одного экрана
	* Поля:
		* surface: pygame.Surface
		* saveData: SaveData
		* world: str
		* tiles: list\[list\[Tile]]
		* entities: list\[Entity]
	* Методы:
		1. init(world: str, coords: tuple[int, int])
		2. calc(player: SptitePlayer) -> None | ScreenGoTo - вызов calc у всех entities и у player
		3. draw(player: SptitePlayer) -> pygame.Surface - вызов draw у всех entities и у player, возвращает итоговый кадр
---
10. Класс ScreenGoTo
	* То куда необходимо переключить экран и его изображение
	* Поля:
		* world: str
		* screen: tuple[int, int]
		* image: pygame.Surface - изображение последнего кадра этого экрана
	* Методы:
		1. init(world: str, screen: tuple[int, int], image: pygame.Surface)
---
11. Класс ScreenMove
	* Хранит информацию для плавной смены экранов
	* Поля:
		* surface: pygame.Surface - холст для отрисовки кадра
		* imageOld: pygame.Surface - предыдущий экран
		* imageNew: pygame.Surface - новый экран
		* dx: float - сдвиг экранов
		* dy: float
		* speedX: float - скорость сдвига
		* speedY: float
	* Методы:
		1. init(imageOld: pygame.Surface, imageNew: pygame.Surface, direction: tuple\[int, int]) - direction - значения 1, 0 или -1 сдвиг по x или y. На основе direction установка dx, dy и скорости
		2. calc() -> bool - возвращает флаг закончилась ли анимация
		3. draw() -> pygame.Surface - возвращает кадр анимации сдвига
---
12. Класс Overlay
	* Вывод информации про количество жизней, инвентарь, кнопка? "Сохранить и выйти"
	* Поля:
		* surface: pygame.Surface
		* player: SptitePlayer
	* Методы:
		1. init(player: SptitePlayer)
		2. calc() -> bool - возвращает True, если игрок нажал "Выйти"
		3. draw() -> pygame.Surface
---