# Кактусы

## tags
* quest-cactus-started
* quest-cactus-1
* quest-cactus-2
* quest-cactus-3
* quest-cactus-4
* quest-cactus-ended


## Главный кактус
1. В tags присутствует **quest-cactus-ended**:
	* При ударе:
		* Режим танца
		* Музыка
	* Если играет музыка:
		* Режим танца

2. В tags отсутствует **quest-cactus-started**:
	* Текст с просьбой о помощи (0)
	* tags < **quest-cactus-started**

3. В tags присутствует **quest-cactus-started**:
	* X = кол-во quest-cactus-N в tags
	* Если X == 4:
		* Текст с благодарностью (9)
		* tags < **quest-cactus-ended**
		* Режим танца
		* Музыка
	* Иначе:
		* Текст с просьбой найти ещё X кактусов (5-8)

## Остальные кактусы
1. В tags присутствует **quest-cactus-ended**:
	* При ударе:
		* Режим танца
		* Музыка
	* Если играет музыка:
		* Режим танца

2. В tags отсутствует **quest-cactus-started**:
	* При ударе: Ничего

3. В tags присутствует **quest-cactus-ЦветКактуса**:
	* Текст с благодарностью (1-4)

4. В tags присутствует **quest-cactus-started**:
	* Текст с благодарностью (1-4)
	* tags < **quest-cactus-ЦветКактуса**


# Пират

## tags
* quest-pirate-started
* quest-pirate-tubeFound
* quest-pirate-ended

## Пират
1. В tags присутствует **quest-pirate-ended**:
	* Текст с благодарностью (2)

2. В tags отсутствует **quest-pirate-tubeFound** и отсутствует **quest-pirate-started**:
	* Приветствие (0)
	* Текст с просьбой о помощи (1)
	* tags < **quest-pirate-started**

3. В tags отсутствует **quest-pirate-tubeFound** и присутствует **quest-pirate-started**:
	* Текст с просьбой о помощи (1)

4. В tags присутствует **quest-pirate-tubeFound** и отсутствует **quest-pirate-started**:
	* Приветствие (0)
	* Текст с просьбой о помощи (1)
	* Текст с благодарностью (2)
	* tags < **quest-pirate-started**
	* tags < **quest-pirate-ended**

5. В tags присутствует **quest-pirate-tubeFound** и присутствует **quest-pirate-started**:
	* Текст с благодарностью (2)
	* tags < **quest-pirate-ended**

## Подзорная труба
* При нахождении:
	* tags < **quest-pirate-tubeFound**
