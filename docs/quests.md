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
	* В виде человечка
	* При ударе:
		* Режим танца
		* Музыка
	* Если играет музыка:
		* Режим танца

2. В tags отсутствует **quest-cactus-started**:
	* В виде кактуса
	* Текст с просьбой о помощи (0)
	* tags < **quest-cactus-started**

3. В tags присутствует **quest-cactus-started**:
	* В виде человечка
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
	* В виде человечка
	* При ударе:
		* Режим танца
		* Музыка
	* Если играет музыка:
		* Режим танца

2. В tags отсутствует **quest-cactus-started**:
	* В виде кактуса
	* При ударе: Ничего

3. В tags присутствует **quest-cactus-ЦветКактуса**:
	* В виде человечка
	* Текст с благодарностью (1-4)

4. В tags присутствует **quest-cactus-started**:
	* В виде кактуса
	* Текст с благодарностью (1-4)
	* tags < **quest-cactus-ЦветКактуса**


# Пират

## tags
* quest-pirate-tubeFound
* quest-pirate-ended

## Пират
1. В tags присутствует **quest-cactus-ended**:
	* Текст с благодарностью (1)

2. В tags отсутствует **quest-cactus-tubeFound**:
	* Текст с просьбой о помощи (0)

3. В tags присутствует **quest-cactus-tubeFound**:
	* Текст с благодарностью (1)
	* tags < **quest-pirate-ended**

## Подзорная труба
* При нахождении:
	* tags < **quest-pirate-tubeFound**
