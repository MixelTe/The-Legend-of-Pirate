1. Класс Main
	* Создаётся на старте программы и вызывается метод start
	* Поля:
		* screen: Surface - Главный холст
		* window: Window - Текущее окно. При старте: WindowStart
	* Методы:
		1. init() - создание окна 1920x1080 в полноэкранном режиме
		2. start() - запуск игрового цикла.
			* Цикл вызывает методы on_event, calc и draw у window. Если функция calc возвращает Window, то текущее окно заменяется на него.
			* Для работы контроллеров (gamepad):
				```python
				pygame.joystick.init()
				```
				В игровом цикле (для (пере)подключения контроллера):
				```python
				for i in range(pygame.joystick.get_count()):
        			pygame.joystick.Joystick(i).init()
				```
				События контроллера: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION
---
2. Класс Settings
	* Содержит все системные настройки игры
	* Поля:
		* width = 1920
		* height = 1080
		* overlay_height: int
		* folder_data = "data"
		* folder_save = "save"
		* folder_images = "images"
		* folder_worlds = "worlds"
		* screen_width = 15
		* screen_height = 7
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
		* player: EntityPlayer
		* world: World
		* screen: Screen
		* screenAnim: ScreenAnimationMove | None
		* overlay: Overlay
		* worlds: Dict[str, World] - Все миры
	* Методы:
		1. init(mainSurface: pygame.Surface, save: int) - загрузка сохранения и создание текущего мира и экрана
		2. on_event(event: Event) - вызывает методы player.keyDown(key) и player.keyUp(key), при соответствующих событиях
		3. calc() -> None | Window
			* Если screenAnim не None, то (пропуская пункты ниже) вызывает screenAnim.calc(). Если метод возвращает True, то присваеваит None в screenAnim.
			* Вызывает screen.calc() если метод возвращает ScreenGoTo, то переключает эран на требуемый: если мир тот же, то создаётся следующий экран и ScreenAnimationMove, если мир другой, то создаётся новый мир, экран и ScreenAnimationBlur. Обновляет информацию в saveData
			* Вызывает overlay.calc(), если метод возвращает True, то вызывает saveData.save() и возвращает WindowStart(mainSurface, save)
			* Проверяет кол-во жизней у игрока. Если их <= 0, то вызывает saveData.save() и возвращает WindowEnd(mainSurface, save)
		4. draw() - Если screenAnim None, то вызывет screen.draw() и выводит полученую картинку на экран, иначе выводит screenAnim.next(). Выводит на экран overlay.draw()
---
8. Класс SaveData
	* Все данные, необходимые для сохранения прогресса игрока
	* Поля:
		* save: int - ячейка сохранения
		* saveVersion: int - версия файла сохранения
		* checkPointX: int
		* checkPointY: int
		* world: str - мир в котором находится точка сохранения
		* screen: tuple[int, int] - экран на котором находится точка сохранения
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
		checkPointX checkPointY
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
	* Логика и отрисовка одного экрана
	* Поля:
		* surface: pygame.Surface - размер: (Settings.width, Settings.height - Settings.overlay_height)
		* saveData: SaveData
		* world: World
		* tiles: list\[list\[Tile]]
		* entities: list\[Entity]
		* goTo: ScreenGoTo | None
	* Методы:
		1. init(world: World, data: ScreenData, saveData: SaveData, player: EntityPlayer) - добавляет player в список entities
		2. calc() -> None | ScreenGoTo - вызов calc у всех entities. Возвращает goTo.
		3. draw() -> pygame.Surface - вызов draw у всех entities, возвращает итоговый кадр
		4. addEntity(entity: Entity) -> добавляет entity в их список
		5. removeEntity(entity: Entity) -> удаляет entity из списка
		6. goTo(world: str, screen: tuple[int, int]) - создаёт ScreenGoTo и присваивает в goTo
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
11. Класс ScreenAnimation
	* Анимация для плавной смены экранов
		* surface: pygame.Surface - холст для отрисовки кадра
	* Методы:
		2. calc() -> bool - возвращает флаг закончилась ли анимация
		3. draw() -> pygame.Surface - возвращает кадр анимации сдвига
---
12. Класс ScreenAnimationMove(ScreenAnimation)
	* Анимация сдвига экрана
	* Поля:
		* imageOld: pygame.Surface - предыдущий экран
		* imageNew: pygame.Surface - новый экран
		* dx: float - сдвиг экранов
		* dy: float
		* speedX: float - скорость сдвига
		* speedY: float
	* Методы:
		1. init(imageOld: pygame.Surface, imageNew: pygame.Surface, direction: tuple\[int, int]) - direction - значения 1, 0 или -1 сдвиг по x или y. На основе direction установка dx, dy и скорости
---
13. Класс ScreenAnimationBlur(ScreenAnimation)
	* Анимация смены экрана
	* Поля:
		* imageOld: pygame.Surface - предыдущий экран
		* imageNew: pygame.Surface - новый экран
		* dx: float - сдвиг экранов
		* dy: float
		* speedX: float - скорость сдвига
		* speedY: float
	* Методы:
		1. init(imageOld: pygame.Surface, imageNew: pygame.Surface, direction: tuple\[int, int]) - direction - значения 1, 0 или -1 сдвиг по x или y. На основе direction установка dx, dy и скорости
---
14. Класс Overlay
	* Вывод информации про количество жизней, инвентарь, кнопка "Сохранить и выйти"
	* Поля:
		* surface: pygame.Surface
		* player: EntityPlayer
	* Методы:
		1. init(player: EntityPlayer)
		2. calc() -> bool - возвращает True, если игрок нажал "Выйти"
		3. draw() -> pygame.Surface
---
15. Класс Entity
	* Базовый класс сущности
	* Поля:
		* screen: Screen - экран, для доступа к списку сущностей и к клеткам мира
		* x: float
		* y: float
		* width: int
		* height: int
		* speed: float - скорость сущности
		* speedX: float - текущая скорость
		* speedY: float
		* image: pygame.Surface
		* hitbox: pygame.Rect - область для просчёта столкновений, относительно сущности.
		* static entityDict: dict[str, class] - словарь всех Entity для метода Entity.fromData
	* Методы:
		1. init(screen: Screen)
		2. static fromData(data: dict) -> Entity - создаёт сущность из данных. И вызывает у него applyData(data)
		3. applyData(data: dict) - установка значений полей из соответствующих полей данных
		3. calc()
		4. draw(surface: pygame.Surface)
		5. move() -> None | Entity - просчёт движения с учётом карты и сущностей. При столкновении с сущностью возвращает эту сущность
		6. remove() - удаляет себя из списка сущностей
---
16. Класс World
	* Хранит информацию о игровом мире
	* Поля:
		* name: str
		* size: tuple[int, int]
		* screens: dict[(int, int), ScreenData]
	* Методы:
		1. init(name: str) - загрузка ScreenData и size
		2. screenExist(x, y) -> bool - проверка существует ли экран с такими координатами
		3. createScreen(x, y, saveData: SaveData, player: EntityPlayer) -> Screen
	* Хранение мира:
		* В папке worlds файл worldName.txt:

			```width height```

		* В папке worlds папка worldName с экранами этого мира
---
17. Класс ScreenData
	* Хранит информацию об одном экране
	* Поля:
		* tiles: list[list[str]] - строка - id Tile`а
		* entity: list[dict] - словарь с информацией о сущности
	* Формат хранения:
		* В папке worldName файл "x;y.json":
		```
		{
			tiles: [["tileId"]],
			entity: [{
					class: "className",
					x: number,
					y: number
				}
			]
		}
		```
		* В данных сущности могут быть любые дополнительные поля, необходимые для сущности.
---
18. Класс EntityPlayer(Entity)
	* Поля:
		* health: int
		* coins: int
		* buttonPressed: [bool, bool, bool, bool] - Нажаты ли кнопки движения в направлениях: вверх, вправо, вниз, влево (для корректного изменения направления движения)
		* weapon: Entity | None - оружее при ударе
	* Методы:
		* onKeyDown(key)
		* onKeyUp(key)
		* onJoyHat(value)
		* onJoyButonDown(button)
		* onJoyButonUp(button)
---
19. Класс Animator
	* Аниматор сущностей
	* Поля:
		* image: pygame.Surface - картинка с анимациями, каждая анимация на новой строке
		* frameSize: tuple[int, int]
		* animation: list\[tuple[int, int]] - tuple[скорость переключения кадров, кол-во кадров] для каждой анимации.
		* frame: tuple[int, int] - tuple[строка, картинка]
		* counter: int - счетчик для переключения кадров с определённой скоростью
		* names: list\[str] - названия анимаций
	* Методы:
		* init(image: pygame.Surface, frameSize: tuple[int, int], animation: list\[int, int])
		* setNames(names: list\[str]) - устанавливает название для каждой анимации
		* calc() -> tuple[bool, bool] - прибавляет счётчик, и переключает кадр, если прошло достаточно времени. После последнего кадра идёт первый.

			Возвращает два значения:
			* Был ли переключён кадр
			* Поледний ли это кадр анимации
		* getImage() -> pygame.Surface - возвращает текущий кадр
		* setAnimation(animation: int | str) - устанавливает текущую анимацию по номеру или её названию
		* curAnimation() -> tuple[int, str | None] - номер и название (если есть, иначе None) текущей анимации
---