# Написание сущностей
Все сущности находятся в папке **src/game/entities**

# Базовая сущность
Существует два вида сущностей: обычные и живые (могут наносить и получать урон).

Все размеры и координаты указываются в клетках (не в пикселях).

## Создание сущности
```py
from game.entity import Entity

class EntityCoolName(Entity):
	pass
```

У такой сущности будет размер 1 на 1 клетку, скорость 0, и у неё не будет картинки.

## Живая сущность
```py
from game.entity import EntityAlive, EntityGroups

class EntityCoolNameAlive(EntityAlive):
	pass
```

У такой сущности будет сила атаки 0 и кол-во hp - 1

## Регистрация сущности
Для того, чтобы сущность появилась в игре её необходимо зарегистрировать.
```py
from game.entity import Entity

class EntityCoolName(Entity):
	pass

Entity.registerEntity("coolName", EntityCoolName)
```
Если сущность с таким id уже существует, произойдёт ошибка

В **game/entity.py** необходимо так же дописать import в функцию loadEntities (в самом конце файла):
```py
def loadEntities():
	# import других сущностей
	import game.entities.название_файла_с_вашей_сущностью
```

## Настройка Сущности
```py
class EntityCoolName(Entity):
    def __init__(self, screen, data=None):
        super().__init__(screen, data)
        self.свойство = значение
```

Все настраиваемые поля обычной сущности (Entity):

Поле   | Описание      | Значение       | По умолчанию
-------|---------------|----------------|-------------
x      | позиция по x  | float          | 0
y      | позиция по y  | float          | 0
width  | ширина        | float          | 1
height | высота        | float          | 1
speedX | скорость по x | float          | 0
speedY | скорость по y | float          | 0
drawPriority | приоритет отрисовки, чем больше, тем позже рисуется. То есть выше остальных | int | 1
hidden | если True, то остальные сущности перестают проверять столкновения с этой сущностью | bool | False
ghostE | если True, то на движение сущности не влияют другие |  bool | False
ghostT | если True, то на движение сущности не влияют клетки | bool | False
image  | картинка      | pygame.Surface | None
imagePos | позиция картинки относительно сущности | tuple[float, float] | (0, 0)
animator | анимации | Animator | None

Дополнительные настраиваемые поля для живой сущности (EntityAlive):

Поле      | Описание           | Значение | По умолчанию
----------|--------------------|----------|-------------
health    | hp                 | int      | 1
healthMax | максимальное hp    | int      | 1
strength  | сила удара         | int      | 0
alive     | жива ли            | bool     | True
immortal  | игноририет ли урон | bool     | False
removeOnDeath | удалять ли после смерти | bool | True
attackPushback | действует ли отталкивание от удара | bool | True
group     | группа             |          | EntityGroups.neutral

alive - если False, то начинается анимация гибели, после которой сущность удаляется.

group - группа, к которй относиться сущность. Для определения кто кому может наносить урон.

Группа                  | Кто             | Кого бьёт
------------------------|-----------------|----------
EntityGroups.neutral    | Например кактус | player, enemy, playerSelf
EntityGroups.player     | Все союзники    | enemy, neutral
EntityGroups.enemy      | Все противники  | player, playerSelf
EntityGroups.playerSelf | Игрок           |

У каждой сущности есть поле id

## Картинка сущности
Для добавления картинки её необходимо положить в папку **src/data/images/entities**

Для загрузки изображения используется функция load_entityImg, с параметрами:
1. название файла
2. требуемая ширина картинки (в клетках)
3. требуемая высота
```py
class EntityCoolName(Entity):
    image = load_entityImg("image_name.png", 1, 1)

    def __init__(self, screen, data=None):
        super().__init__(screen, data)
        self.image = EntityCoolName.image
```

## Загрузка данных
Если у сущности есть параметры, которые сохранены в файле с миром, то их необходимо получить из данных, которые передаются сущности при создании.

Для этого необходимо модифицировать функцию **applyData**
Она получает словарь данных. Словарь не равен None.
```py
class EntityCoolName(Entity):
    def applyData(self, data: dict):
        super().applyData(data)
        if ("nickname" in data):
            self.myCoolNickname = data["nickname"]
```
**super().applyData(data)** - присваевает x и y из данных

## Анимации
### Картинки
Для добавления анимаций их необходимо положить в папку **src/data/images/entities/название_сущности**

Каждая картинка должна называться так же, как анимация

В каждой картинке должны быть все кадры анимации в одну строку без промежутков между кадрами. Каждый кадр должен быть одинакогово размера.

Пример картинки с анимацией:

![](imgs/animation.png)

Между пиратами есть промежуток, так как размер кадра должен быть одинаковый.
В том месте, где у первого пирата пусто, у последнего лопата.

В разных анимациях размер и кол-во кадров не обязаны совпадать.

### Загрузка
Для загрузки анимаций необходимо создать AnimatorData, вне класса (или статическим полем):

```py
from game.animator import Animator, AnimatorData

animatorData = AnimatorData("папка_с_анимаиями", [])

class EntityCoolName(Entity):
	pass
```

Вторым параметром AnimatorData принемает список всех анимаций.
Каждый елемент списка - это tuple из четырёх элементов:
1. str - название файла с анимацией
2. int - промежуток между кадрами анимации (в милисекундах)
3. tuple[int, int] - размер одного кадра анимации в картинке с анимацией (в пикселях)
4. tuple[float, float, float, float] - позиция картинки относительно сущности и размер требуемой картинки (в клетках) - (x, y, w, h)

Пример:
```py
animatorData = AnimatorData("cool_entity", [
    ("going.png", 150, (12, 24), (0, -0.5, 0.75, 1.5)),
])
```
Аниматор:
1. Загрузит картинку **going.png** из папки **src/data/images/entities/cool_entity**
2. Разделит её на кадры размером 12 на 24
3. Увеличит каждый кадр до размера 0.75 на 1.5 (клеток)
4. Сохранит анимацию под именем **going**

### Использование
Сущности необходимо создать Animator

```py
animatorData = AnimatorData("папка_с_анимациями", [
    ("going.png", 150, (12, 24), (0, -0.5, 0.75, 1.5)),
    # и другие
])

class EntityCoolName(Entity):
    def __init__(self, screen, data=None):
        super().__init__(screen, data)
        self.animator = Animator(animatorData, "название анимации")
```

У Animator есть методы:
* setAnimation("название анимации") - запустить анимацию
* curAnimation() - возвращает название текущей анимации

Методы, которые вызываются автоматически:
* get_image() -> tuple[pygame.Surface, tuple[int, int]] - текущий кадр и его положение относительно сущности
* update() -> tuple[bool, bool] - (Был ли переключён кадр, Поледний ли был кадр анимации)
И поле:
* lastState: tuple[bool, bool] - последнее значение, возвращенное методом update


# Сущность с "кодом"
Для всего, что сложнее, чем кактус, необходимо модифицировать работу сущности.

## Изменение отрисовки сущности
Для этого необходимо модифировать функцию draw.

```py
class EntityCoolName(Entity):
    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
```
**super().draw(surface)** рисует картинку сущности (если есть).

Если необходимо убрать стандартную отрисовку, то нужно обязательно в конце отрисовки вызвать метод ```self.draw_dev(surface)```

Для отображения прямоугольников есть функция

```py
self.draw_rect(self, surface: pygame.Surface, color: str, rect: tuple[float, float, float, float], fill=False, mul=False, rel=False)
```
mul - умножать ли значения на размер клетки

rel - рисовать относительно сущности

## Установка запретных клеток

Метод **canGoOn** вызывается для каждой клетки, если он возвращает False - клетка считается стеной.

Необходимо учитывать клетки, которые вляются стенами (solid)

```py
class EntityCoolName(Entity):
    def canGoOn(self, tile: Tile) -> bool:
        return not tile.solid # По умолчанию сущность может ходить по всем клеткам, которые не solid
```

## Установка скорости для клеток

Метод **tileSpeed** вызывается для каждой клетки, скорость движения умножается на возвращаемое значение.

```py
class EntityCoolName(Entity):
    def tileSpeed(self, tile: Tile) -> float:
        return tile.speed # По умолчанию используется скорость клетки
```

## Изменение поведения
Для этого необходимо модифировать функцию update.

```py
class EntityCoolName(Entity):
    def update(self):
        super().update()
```

**super().update()** - обновляет аниматор и просчитывает положение сущности по текущей скорости.
Возвращает список столкновений, в котором каждый элемент - это tuple из прямоугольника с которым столкнулась сущность и объектом, с которым столкнулась (Entity, Tile или None (столкновение с краем экрана))

Пример проверки столкновения с игроком, с клеткой глубокой воды

```py
class EntityCoolName(Entity):
    def update(self):
        collisions = super().update()

        for rect, collision in collisions:
            if (collision is not None):
                if (collision.id == "player"):
                    print("Столкновение с игроком")
                elif (collision.id == "water_deep"):
                    print("Столкновение с глубокой водой")
```

Для создания сущности, не подчиняющейся законам физики, необходимо убрать вызов метода **super().update()**. При этом будет необходимо будет самостоятельно прочитывать движение сущности.

Метод **canPassThrough** вызывается для каждой сущности при столкновении, если он возвращает True - текущая сущность проходит сквозь данную (как будто не сталкивались).

Все противники должны перестовать атаковать игрока, если значение self.screen.player.visibleForEnemies не True

## Взаимодействие с миром
Для создания сложных сущностей потребуятся данные о мире и способы взаимодействовать с ним.

В поля помеченные в списке буквой **W** можно присваивать значения

* self.get_tile() - получить клетку на которой стоит сущность и её координаты

* self.get_tile(dx: int, dy: int) - получить клетку относительно сущности

* self.get_tile(pos=(0.5, 0.5)) - получить клетку на которой стоит сущность, позиция сущности определяется как координаты верхнего левого угла плюс ширина и высота сущности, умноженные на **pos**. При значении (0.5, 0.5), будет возвращена клетка под центром сущности.

* self.get_entities(rect: tuple[float, float, float, float]) - получить сущностей попадающих в данную область

* self.createById(id: str, screen: pygame.Surface) - создать сущность по id

* self.remove() - удалить эту сущность

* self.is_inRect(rect: tuple[float, float, float, float]) - проверка попадает ли эта сущность в область

* self.is_inRectD(rect: tuple[float, float, float, float], entity: Entity) - проверка попадает ли сущность в область, относительную этой

* self.predictCollisions(x: float, y: float) - возвращает столкновения, если бы сущность была расположена по этим координатам

* self.screen.addEntity(entity: Entity) - добавить сущность в мир

* self.screen.removeEntity(entity: Entity) - удалить сущность из мира

* self.screen.goTo(world: str, screen: tuple[int, int], pos?: tuple[int, int]) - переключить экран, если такого нет, произойдёт ошибка. world - id мира, screen - координаты экрана, pos - новые координаты игрока (необязательный параметр).

* self.screen.world.name - id текущего мира

* self.screen.world.size - размер текущего мира

* self.screen.world.screenExist(x: int, y: int) - проверка, существует ли экран с такими координатами

* self.screen.tryGoTo(dir: "up" | "right" | "down" | "left") - переключить экран на соседний. Если такого нет, ничего не произойдёт.

* self.screen.getTiles() -> итератор всех клеток, где каждый элемент - это (tile, x, y)

* self.screen.entities - список всех сущностей

* self.screen.openDialog(dialog: GameDialog) - открыть диалоговое окно

* self.screen.pos - позиция экрана (в мире)

* self.screen.saveData - данные сохранения мира (SaveData)

* self.screen.player - игрок (EntityPlayer)

* **W** self.screen.player.message - сообщение, которое выводится игроку (для показа сообщения необходимо присваивать его при каждом update)

* **W** self.screen.player.action - функция, которая будет вызвана, при нажатии кнопки действия. Например, когда игрок подходит к предмету торговца, в это поле присваиватся функция покупки. (необходимо присваивать при каждом update)

* **W** self.screen.player.messageIsLong - если в self.screen.player.action вы присвоили функцию, переключающее сообщение на следущее, то присвойте сюда True, тогда игроку покажется иконка, подсказывающая, что можно переключить сообщение. (необходимо присваивать при каждом update)

* self.screen.player.takeItem(item: Entity, onAnimEnd: () => None = None) - активировать анимацию взятия предмета. Игроку отобразиться то изображение, которое находиться в item.image (если его поменять во время анимации, то и в анимации оно изменится). По завершению анимации будет вызвана функция onAnimEnd, если вы её передали.

* self.screen.player.takeItemFun(size: tuple[float, float], drawFun: (pygame.Surface, float, float, float) => None, onAnimEnd: () => None = None) - тоже активировать анимацию взятия предмета, но рисовать предмет нужно своей функцией drawFun, которой передаются параметры: pygame.Surface, x, y, размер объекта (от 0 до 1). По завершению анимации будет вызвана функция onAnimEnd, если вы её передали.
