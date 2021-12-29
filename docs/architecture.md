1. ## Класс Main
	* Создаётся на старте программы и вызывается метод start
	* Поля:
		* screen: pygame.Surface - Главный холст
		* window: Window - Текущее окно. При старте: WindowStart
	* Методы:
		1. init() - создание окна 1920x1080 в полноэкранном режиме
		2. start() - запуск игрового цикла.
			* Цикл вызывает методы on_event, update и draw у window. Если функция update возвращает Window, то текущее окно заменяется на него.
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
2. ## Класс Settings
	* Содержит все системные настройки игры
	* Поля:
		* width = 1920
		* height = 1080
		* fps = 30
		* overlay_height: int
		* folder_data = "data"
		* folder_save = "save"
		* folder_images = "images"
		* folder_worlds = "worlds"
		* screen_width = 15
		* screen_height = 7
		* demageDelay = 400 (миллисекунды)
---
3. ## Класс Window
	* Базовый класс окна
	* Методы:
		1. on_event(event: Event) - обрабатывает событие
		2. update() -> None | Window - просчитывает новый кадр
		3. draw(screen: pygame.Surface) - рисует текущий кадр
---
4. ## Класс WindowStart(Window)
	* Стартовое окно.
	* Поля:
		* save: int - ячейка сохранения
	* Методы:
		1. init(save: int = 1)
	* Кнопки:
		2. "Старт" - запуск игры, при нажатии метод update возвращает WindowGame(mainSurface, save)
		3. "Статистика" - при нажатии метод update возвращает WindowStatistics(mainSurface, save)
		4. Выбор ячейки сохранения - три кнопки: "1", "2" и "3". При нажатии на кнопки save меняется на соответствующее значение.
		5. "Выйти" - при нажатии создаёт событие quit.
		```python
		pygame.event.post(pygame.event.Event(pygame.QUIT))
		```
---
5. ## Класс WindowStatistics(Window)
	* Отображает статистику текущего сохранения
	* Поля:
		* save: int - ячейка сохранения
	* Методы:
		1. init(save: int)
	* Кнопки:
		2. "Назад" - при нажатии метод update возвращает WindowStart(mainSurface, save)
---
6. ## Класс WindowEnd(Window)
	* Финальный экран. Возможно титры или просто благодарность за игру. Включается после победы над боссом. После показа титров или нажатия кнопки "Продолжить" метод update возвращает WindowStatistics(mainSurface, save)
	* Поля:
		* save: int - ячейка сохранения
	* Методы:
		1. init(save: int)
---
7. ## Класс WindowGame(Window)
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
		* time: datetime - время запуска игры для сохранения времени игры
	* Методы:
		1. init(mainSurface: pygame.Surface, save: int) - загрузка сохранения и создание текущего мира и экрана
		2. on_event(event: Event)
			* вызывает методы player.keyDown(key), player.keyUp(key), player.onJoyHat(value), player.onJoyButonDown(button), player.onJoyButonUp(button), при соответствующих событиях. Если screenAnim == None.
			* вызывает метод overlay.onClick(pos) при нажатии.
		3. update() -> None | Window
			* Если screenAnim не None, то (пропуская пункты ниже) вызывает screenAnim.update(). Если метод возвращает True, то присваеваит None в screenAnim.
			* Вызывает screen.update() если метод возвращает ScreenGoTo, то переключает эран на требуемый: если мир тот же, то создаётся следующий экран и ScreenAnimationMove, если мир другой, то создаётся новый мир, экран и ScreenAnimationBlur. Обновляет информацию в saveData. Присваетвает новый экран в player.screen
			* Вызывает overlay.update(), если метод возвращает True, то вызывает saveData.save() и возвращает WindowStart(mainSurface, save)
			* Проверяет кол-во жизней у игрока. Если их <= 0, то вызывает saveData.save() и возвращает WindowEnd(mainSurface, save)
		4. draw(screen: pygame.Surface) - Если screenAnim None, то вызывет screen.draw() и выводит полученую картинку на экран, иначе выводит screenAnim.next(). Выводит на экран overlay.draw() и self.screen.draw()
---
8. ## Класс SaveData
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
		* bullets: int
		* time: int - время игры в секундах
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
		bullets
		time
		// тэги, в одну строку, через точку с запятой (;)
		";".join(tags)
		```
---
9. ## Класс Screen
	* Логика и отрисовка одного экрана
	* Поля:
		* surface: pygame.Surface - размер: (Settings.width, Settings.height - Settings.overlay_height)
		* saveData: SaveData
		* world: World
		* tiles: list\[list\[Tile]]
		* entities: list\[Entity]
		* goToVar: ScreenGoTo | None
	* Методы:
		1. init(world: World, data: ScreenData, saveData: SaveData, player: EntityPlayer) - добавляет player в список entities
		2. update() -> None | ScreenGoTo - вызов update у всех entities. Возвращает goToVar.
		3. draw() -> pygame.Surface - вызов draw у всех entities, возвращает итоговый кадр
		4. addEntity(entity: Entity) -> добавляет entity в их список
		5. removeEntity(entity: Entity) -> удаляет entity из списка
		6. goTo(world: str, screen: tuple[int, int]) - создаёт ScreenGoTo и присваивает в goToVar
---
10. ## Класс ScreenGoTo
	* То куда необходимо переключить экран и его изображение
	* Поля:
		* world: str
		* screen: tuple[int, int]
		* image: pygame.Surface - изображение последнего кадра этого экрана
	* Методы:
		1. init(world: str, screen: tuple[int, int], image: pygame.Surface)
---
11. ## Класс ScreenAnimation
	* Анимация для плавной смены экранов
		* surface: pygame.Surface - холст для отрисовки кадра
	* Методы:
		2. update() -> bool - возвращает флаг закончилась ли анимация
		3. draw() -> pygame.Surface - возвращает кадр анимации сдвига
---
12. ## Класс ScreenAnimationMove(ScreenAnimation)
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
13. ## Класс ScreenAnimationBlur(ScreenAnimation)
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
14. ## Класс Overlay
	* Вывод информации про количество жизней, инвентарь, кнопка "Сохранить и выйти"
	* Поля:
		* surface: pygame.Surface
		* player: EntityPlayer
	* Методы:
		1. init(player: EntityPlayer)
		2. update() -> bool - возвращает True, если игрок нажал "Выйти"
		3. draw() -> pygame.Surface - если player.message не пусто, то выводится это сообщение.
		4. onClick(pos)
---
15. ## Класс Entity
	* Базовый класс сущности
	* Поля:
		* screen: Screen - экран, для доступа к списку сущностей и к клеткам мира
		* group: int - группа к которой пренадлежит сущность, для определения нужно ли наносить урон (присваивать значение только с помощью полей класса EntityGroups)
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
		3. update()
		4. draw(surface: pygame.Surface)
		5. move() -> None | Entity | Tile - просчёт движения с учётом карты и сущностей. При столкновении с сущностью или клеткой возвращает эту сущность или клетку
		6. remove() - удаляет себя из списка сущностей
	* Класс EntityGroups:
		* Группы сущностей
		* Поля:
			* neutral = 0
			* player = 1
			* enemy = 2
---
16. ## Класс EntityAlive(Entity)
	* Поля:
		* animator: Animator
		* health: int
		* damageDelay: int - при вызове update уменьшается на 1000 / Settings.fps
	* Методы:
		* takeDamage(damage: int) - Уменьшение здоровья и установка damageDelay в Settings.damageDelay, если damageDelay <= 0
---
17. ## Класс World
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
18. ## Класс ScreenData
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
19. ## Класс EntityPlayer(EntityAlive)
	* Поля:
		* coins: int
		* bullets: int
		* buttonPressed: [bool, bool, bool, bool] - нажаты ли кнопки движения в направлениях: вверх, вправо, вниз, влево (для корректного изменения направления движения)
		* weapon: Entity | None - оружее при ударе
		* message: str - сообщение, которое выведится игроку
	* Методы:
		* init() - присваивает None в screen
		* update() - пропускается если screen == None
		* onKeyDown(key)
		* onKeyUp(key)
		* onJoyHat(value)
		* onJoyButonDown(button)
		* onJoyButonUp(button)
---
20. ## Класс Animator
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
		* update() -> tuple[bool, bool] - прибавляет счётчик, и переключает кадр, если прошло достаточно времени. После последнего кадра идёт первый.

			Возвращает два значения:
			* Был ли переключён кадр
			* Поледний ли это кадр анимации
		* getImage() -> pygame.Surface - возвращает текущий кадр
		* setAnimation(animation: int | str) - устанавливает текущую анимацию по номеру или её названию
		* curAnimation() -> tuple[int, str | None] - номер и название (если есть, иначе None) текущей анимации
---
21. ## Класс Tile
	* Одна клетка на экране
	* Поля:
		* static tileIds: dict[str, Tile]
		* image: pygame.Surface
		* speed: float - множитель скорости клетки
		* digable: bool - можно ли копать на этой клетке
		* solid: bool - плотная ли клетка (стена)
	* Методы:
		* init(image: str, solid: bool = False, digable: bool = False, speed: float = 1) - добавляет себя в tileIds по ключу image отрезав расширение файла (всё после первой точки)
		* static fromId(id: str) -> Tile - получить клетку по id из tileIds
	* Создаёт все клетки на старте программы:
		```
		Tile("img.png", False, True, 1)
		Tile("img.png")
		```
---
## Сущности
---
22. ## Класс EntityShovel(Entity)
	* Лопата, которой бьёт игрок
	* Группа: player
---
23. ## Класс EntityCrab(EntityAlive)
	* Спит пока к нему не подойдёт игрок, потом ходит за игроком. Может уснуть во время погони.
	* Группа: enemy
---
