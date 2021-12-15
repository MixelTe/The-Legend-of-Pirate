1. Класс Main
	* Создаётся на старте программы и вызывается метод start
	* Поля:
		* screen: Surface - Главный холст
		* window: Window - Текущее окно. При старте: WindowStart
	* Методы:
		1. init() - создание окна 1920x1080 в полноэкранном режиме
		2. start() - запуск игрового цикла. Цикл вызывает методы on_event, calc и draw у self.window. Если функция calc возвращает Window, то текущее окно заменяется на него.
---
2. Класс Window
	* Базовый класс окна
	* Поля:
		* mainSurface: pygame.Surface
	* Методы:
		1. init(mainSurface: pygame.Surface)
		2. on_event(event: Event) - обрабатывает событие
		3. calc() -> None | Window - просчитывает новый кадр
		4. draw(screen: Surface) - рисует текущий кадр
---
3. Класс WindowStart(Window)
	* Стартовое окно.
	* Поля:
		* save: int - ячейка сохранения
	* Методы:
		1. init(mainSurface: pygame.Surface, save: int = 1)
	* Кнопки:
		2. "Старт" - запуск игры, при нажатии метод calc возвращает WindowGame(self.mainSurface, self.save)
		3. "Статистика" - при нажатии метод calc возвращает WindowStatistics(self.mainSurface, self.save)
		4. Выбор ячейки сохранения - три кнопки: "1", "2" и "3". При нажатии на кнопки self.save меняется на соответствующее значение.
		5. "Выйти" - при нажатии создаёт событие quit.
		```python
		pygame.event.post(pygame.event.Event(pygame.QUIT))
		```
---
4. Класс WindowStatistics(Window)
	* Отображает статистику текущего сохранения
	* Поля:
		* save: int - ячейка сохранения
	* Методы:
		1. init(mainSurface: pygame.Surface, save: int)
	* Кнопки:
		2. "Назад" - при нажатии метод calc возвращает WindowStart(self.mainSurface, self.save)
---
5. Класс WindowEnd(Window)
	* Финальный экран. Возможно титры или просто благодарность за игру. Включается после победы над боссом. После показа титров или нажатия кнопки "Продолжить" метод calc возвращает WindowStatistics(self.mainSurface, self.save)
	* Поля:
		* save: int - ячейка сохранения
	* Методы:
		1. init(mainSurface: pygame.Surface, save: int)
---
6. Класс WindowGame(Window)
	* Игровой движок
	* Поля:
		* save: int - ячейка сохранения
		* saveData: SaveData
		* player: SptitePlayer
		* world: World
		* screen: Screen
	* Методы:
		1. init(mainSurface: pygame.Surface, save: int) - загрузка сохранения и создание текущего мира и экрана
		2. on_event(event: Event) - вызывает методы player.keyDown(key) и player.keyUp(key), при соответствующих событиях
		2. calc() -> None | Window - вызывает screen.calc(self.player) если метод возвращает ScreenGoTo, то переключает эран на требуемый
---
7. Класс SaveData
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
8. Класс Screen
	* Логика и отрисовка одного экрана
	* Поля:
		* mainSurface: pygame.Surface
		* saveData: SaveData
		* world: str
		* tiles: list\[list\[Tile]]
		* entities: list\[Entity]
	* Методы:
		1. init(world: str, coords: tuple[int, int], mainSurface: pygame.Surface)
		2. calc(player: SptitePlayer) -> None | ScreenGoTo - вызов calc у всех self.entities и у player
		3. draw(player: SptitePlayer) - вызов draw у всех self.entities и у player
---
9. Класс ScreenGoTo
	* То куда необходимо переключить экран и его изображение
	* Поля:
		* world: str
		* screen: tuple[int, int]
		* image: pygame.Surface - изображение последнего кадра этого экрана
