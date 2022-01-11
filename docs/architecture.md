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
				joysticks = []
				for i in range(pygame.joystick.get_count()):
					joystick = pygame.joystick.Joystick(i)
					joystick.init()
					joysticks.append(joystick)
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
	* Стартовое окно
	* Кнопки:
		1. "Старт" - запуск игры, при нажатии метод update возвращает WindowSaveSelection()
		2. "Выйти" - при нажатии создаёт событие quit.
		```python
		pygame.event.post(pygame.event.Event(pygame.QUIT))
		```
---
5. ## Класс WindowSaveSelection(Window)
	* Выбор сохранения для запуска. Отображает статистику всех сохранений.
	* Кнопки:
		1. "Сохранение 1/2/3" - запуск игры, при нажатии метод update возвращает WindowGame(save)
		2. "Назад" - при нажатии метод update возвращает WindowStart()
---
6. ## Класс WindowEnd(Window)
	* Финальный экран. Возможно титры или просто благодарность за игру. Включается после победы над боссом. После показа титров или нажатия кнопки "Продолжить" метод update возвращает WindowStart()
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
		* dialog: GameDialog | None
		* time: datetime - время запуска игры для сохранения времени игры
	* Методы:
		1. init(save: int) - загрузка сохранения и создание текущего мира и экрана
		2. on_event(event: Event)
			* Если dialog не None, то вызывает dialog.on* методы и пропускает следующие пункты
			* вызывает методы player.keyDown(key), player.keyUp(key), player.onJoyHat(value), player.onJoyButonDown(button), player.onJoyButonUp(button), при соответствующих событиях. Если screenAnim == None.
			* вызывает метод overlay.onClick(pos) при нажатии.
		3. update() -> None | Window
			* Вызывает overlay.update(), если метод возвращает True, то вызывает saveData.save() и возвращает WindowStart(mainSurface, save)
			* Если Если dialog не None, вызывает dialog.update() и пропускает следующие пункты, если метод вернул True, то присваевает None в dialog
			* Если screenAnim не None, то (пропуская пункты ниже) вызывает screenAnim.update(). Если метод возвращает True, то присваеваит None в screenAnim.
			* Вызывает screen.update() если метод возвращает ScreenGoTo, то переключает эран на требуемый: если мир тот же, то создаётся следующий экран и ScreenAnimationMove, если мир другой, то создаётся новый мир, экран и ScreenAnimationBlur. Обновляет информацию в saveData. Присваетвает новый экран в player.screen
			* Проверяет кол-во жизней у игрока. Если их <= 0, то вызывает saveData.save() и возвращает WindowEnd(mainSurface, save)
		4. draw(screen: pygame.Surface)
			* Если screenAnim None, то вызывет screen.draw() и выводит полученую картинку на экран, иначе выводит screenAnim.draw()
			* Выводит на экран overlay.draw() и self.screen.draw()
			* Если dialog не None, то выводит на экран dialog.draw()
		5. openDialog: (dialog: GameDialog) -> None - присваевает dialog в self.dialog
---
8. ## Класс SaveData
	* Все данные, необходимые для сохранения прогресса игрока
	* Поля:
		* saveFile: int - ячейка сохранения
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
		* Строка, которая начинается с //, не содержится в файле
		```
		saveVersion
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
		* player: EntityPlayer
		* openDialog: (dialog: GameDialog) -> None
	* Методы:
		1. init(world: World, data: ScreenData, pos: tuple[int, int], saveData: SaveData, player: EntityPlayer, openDialog: (dialog: GameDialog) -> None) - добавляет player в список entities
		2. update() -> None | ScreenGoTo - вызов update у всех entities. Возвращает goToVar.
		3. draw() -> pygame.Surface - вызов draw у всех entities, возвращает итоговый кадр
		4. addEntity(entity: Entity) - добавляет entity в их список
		5. removeEntity(entity: Entity) - удаляет entity из списка
		6. goTo(world: str, screen: tuple[int, int]) - создаёт ScreenGoTo и присваивает в goToVar
		7. static create(world: World, x: int, y: int, saveData: SaveData, player: EntityPlayer, openDialog: (dialog: GameDialog) -> None) -> Screen
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
		* blurState: int
	* Методы:
		1. init(imageOld: pygame.Surface, imageNew: pygame.Surface)
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
		* x: float
		* y: float
		* width: int
		* height: int
		* speedX: float - текущая скорость
		* speedY: float
		* hidden: bool - если True, то остальные сущности перестают проверять столкновения с этой сущностью
		* ghostE: bool - если True, то на движение сущности не влияют другие
		* ghostT: bool - если True, то на движение сущности не влияют клетки
		* animator: Animator
		* image: pygame.Surface
		* imagePos: tuple[int, int] - положение картинки относительно сущности
		* static entityDict: dict[str, class] - словарь всех Entity для метода Entity.fromData
	* Методы:
		1. init(screen: Screen, data: dict=None) - если data не None, вызывает applyData(data)
		2. applyData(data: dict) - установка значений полей из соответствующих полей данных
		3. update()
		4. draw(surface: pygame.Surface)
		5. draw_dev(self, surface: pygame.Surface) - рисует вспомогательную информацию
		6. move() -> None | Entity | Tile - просчёт движения с учётом карты и сущностей. При столкновении с сущностью или клеткой возвращает эту сущность или клетку
		7. remove() - удаляет себя из списка сущностей
		8. static fromData(data: dict, screen: Screen) - создание сущности по данным
		9. static createById(id: str, screen: pygame.Surface) - создание сущности по id
		10. static registerEntity(id: str, entityClass) - добавляет сущность в entityDict
		11. canGoOn(tile: Tile) -> bool - может ли сущность наступить на эту клетку
		12. get_tile(dx: int = 0, dy: int = 0, pos: tuple[float, float] = (0.5, 0.5)) -> Tile | None - клетка относительно сущности. pos - позиция точки проверки в сущности, где 0 - левый верхний угол, 1 - правый нижний
		13. get_entities(rect: tuple[float, float, float, float]) -> list\[Entity] - сущности попадающие в область
		14. get_entitiesD(rect: tuple[float, float, float, float]) -> list\[Entity] - сущности попадающие в область, относительную сущности
---
16. ## Класс EntityAlive(Entity)
	* Поля:
		* group: int - группа к которой пренадлежит сущность, для определения нужно ли наносить урон (присваивать значение только с помощью полей класса EntityGroups)
		* health: int
		* damageDelay: int - при вызове update уменьшается на 1000 / Settings.fps
		* alive: bool - жива ли сущность
	* Методы:
		* takeDamage(damage: int) - Уменьшение здоровья и установка damageDelay в Settings.damageDelay, если damageDelay <= 0
	* Класс EntityGroups:
		* Группы сущностей
		* Поля:
			* neutral = 0
			* player = 1
			* enemy = 2
---
17. ## Класс World
	* Хранит информацию о игровом мире
	* Поля:
		* name: str
		* size: tuple[int, int]
		* screens: list[list[ScreenData | None]]
		* static worlds: Dict[str, World] - Все миры
	* Методы:
		1. init(name: str) - загрузка ScreenData и size
		2. screenExist(x, y) -> bool - проверка существует ли экран с такими координатами
	* Хранение мира:
		* В папке worlds файл worldName.txt, формат хранения:
		```
		map: list[list[ScreenData | None]]
		width: int
		height: int

		ScreenData
		{
			tiles: list[list[string]];
			entity: list[EntityData];
		}
		EntityData
		{
			className: str;
			x: number;
			y: number;
			[a: string]: any;
		}
		```
---
18. ## Класс ScreenData
	* Хранит информацию об одном экране
	* Поля:
		* tiles: list[list[str]] - строка - id Tile`а
		* entity: list[dict] - словарь с информацией о сущности
---
19. ## Класс EntityPlayer(EntityAlive)
	* Поля:
		* buttonPressed: [bool, bool, bool, bool] - нажаты ли кнопки движения в направлениях: вверх, вправо, вниз, влево (для корректного изменения направления движения)
		* weapon: Entity | None - оружие при ударе
		* message: str - сообщение, которое выведится игроку
		* saveData: SaveData
	* Методы:
		* init(saveData: SaveData) - присваивает None в screen
		* update() - пропускается если screen == None
		* onKeyDown(key)
		* onKeyUp(key)
		* onJoyHat(value)
		* onJoyButonDown(button)
		* onJoyButonUp(button)
		* onJoyAxis(axis, value)
		* preUpdate() - вызывается до вызова update у всех сущностей
---
20. ## Класс Animator
	* Аниматор сущностей
	* Поля:
		* data: AnimatorData - все анимации и их кадры
		* anim: str - текущая анимация
		* frame: int - текущий кадр
		* counter: int - счетчик для переключения кадров с определённой скоростью
		* lastState: tuple[bool, bool] - последнее значение, возвращенное методом update
	* Методы:
		* init(data: AnimatorData, anim: str)
		* update() -> tuple[bool, bool] - прибавляет счётчик, и переключает кадр, если прошло достаточно времени. После последнего кадра идёт первый.

			Возвращает два значения:
			* Был ли переключён кадр
			* Поледний ли был кадр анимации
		* getImage() -> tuple[pygame.Surface, tuple[int, int]] - возвращает текущий кадр и его позицию относительно сущности
		* setAnimation(animation: str, frame: int=None) - устанавливает текущую анимацию по её названию, устанавливает кадр в 0 если анимация изменилась, или frame не None
		* curAnimation() -> str - название текущей анимации
## Класс AnimatorData
* Хранит картинки для аниматора сущностей
* Поля:
	* frames: dict[str, tuple[list\[pygame.Surface], int, tuple[int, int]]] - все кадры анимации, скорость переключения кадров (милисекунды между кадрами) и позиция картинки относительно сущности для каждой анимации
* Методы:
	* init(folder: str, animations: list\[tuple[str, int, tuple[int, int], tuple[int, int, int, int]]]) - 
		* folder - папка с анимациями
		* animations - список tuple с содержимом:
			* [0] - название файла с анимацией
			* [1] - промежуток между кадрами (скорость переключения)
			* [2] - размер кадра в анимации
			* [3] - положение относительно сущности и требуемый размер кадра
		* Добавляет каждую анимацию в frames, разделив на кадры и применив масштаб imgSize. Ключ - название файла без расширения
		* Для каждой анимации в animations:
			* Делит картинку [0] на кадры размером [2]
			* Применяет масштаб [3] для каждого кадра
			* В frames\[название_файла_без_расширения] кладёт tuple, с содержимым: 
				* Список со всеми увеличеными кадрами
				* Промежуток между кадрами [1]
				* Положение кадра относительно сущности [3]
	* get_image(animation: str, index: int) - возвращает (frames\[animation]\[0]\[index], frames\[animation]\[2])
	* get_speed(animation: str) - возвращает frames\[animation]\[1]
---
21. ## Класс Tile
	* Одна клетка на экране
	* Поля:
		* static tileIds: dict[str, Tile]
		* image: pygame.Surface
		* speed: float - множитель скорости клетки
		* digable: bool - можно ли копать на этой клетке
		* solid: bool - плотная ли клетка (стена)
		* tags: list\[str] - тэги, например "water"
		* id: str
	* Методы:
		* init(image: str, solid: bool = False, digable: bool = False, speed: float = 1) - добавляет себя в tileIds по ключу image отрезав расширение файла (всё после первой точки)
		* static fromId(id: str) -> Tile - получить клетку по id из tileIds
	* Создаёт все клетки на старте программы:
		```
		Tile("img.png", False, True, 1)
		Tile("img.png")
		```
---
22. ## Класс GameDialog
	* Диалоговое окно, при его открытии игра останавливается
	* Поля:
		* rect: pygame.Rect
	* Метды:
		* init()
		* draw() -> pygame.Surface
		* update() -> bool - закрыт ли диалог
		* on*() - методы для обработки соответствующих событий
---
## Сущности
---
23. ## Класс EntityShovel(Entity)
	* Лопата, которой бьёт игрок
	* Группа: player
---
24. ## Класс EntityCrab(EntityAlive)
	* Спит пока к нему не подойдёт игрок, потом ходит за игроком. Может уснуть во время погони.
	* Группа: enemy
---
