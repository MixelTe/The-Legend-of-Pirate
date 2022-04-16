// name, imgUrl, width, height, widthHitbox, heightHitbox, xImg, yImg, widthImg, heightImg, objData

createNewEntityClass_Auto("crab-kolobok", false, 13, 11, 0.8, 0.677, 0, 0, 0.8, 0.677, [
	{ type: "bool", name: "sleeping", value: true },
	{ type: "number", name: "hp", value: 1, displayColor: "black" },
	{ type: "text", name: "tag", value: null, displayColor: "black", nullable: true },
	{ type: "textAria", name: "description", value: null, displayColor: "black", nullable: true },
	{ type: "aura", name: "atackArea", value: [0.5, 0.5, 1, 1], displayColor: "orange" },
	{ type: "area", name: "sleepArea", value: [6, 2, 5, 3], displayColor: "azure" },
	{ type: "tile", name: "favoriteTile", value: [1, 4], displayColor: "pink" },
	{ type: "tiles", name: "killingTiles", value: [[13, 2], [13, 3]], displayColor: "tomato" },
	{ type: "coords", name: "coords", value: [1, 3], displayColor: "lime" },
]);

createNewEntityClass_Auto("crab", true, 20, 11, 1, 0.55)
createNewEntityClass_Auto("cactus", false, 16, 16, 0.85, 0.85, -0.075, -0.075, 1, 1)
createNewEntityClass_Auto("door", false, 11, 12, 1, 1)
createNewEntityClass_Auto("palm", false, 20, 22, 0.45, 0.7, -0.45, -0.8, 1.5, 1.5)
createNewEntityClass_Auto("trader", true, 14, 24, 0.75, 0.7, 0, -0.8, 0.75, 1.5)
createNewEntityClass_Auto("cannon", true, 11, 12, 1, 1)
createNewEntityClass_Auto("dig_place", false, 7, 7, 1, 1, 0.35, 0.35, 0.3, 0.3, [
	{ type: "text", name: "content", value: "random", options: ["random", "coin", "heart", "crab"], title: "Содержимое" },
])
createNewEntityClass_Auto("trainer", true, 9, 18, 0.75, 0.7, 0, -0.8, 0.75, 1.5)
createNewEntityClass_Auto("pirate2", true, 11, 22, 0.75, 0.7, 0, -0.8, 0.75, 1.5, [
	// { type: "textAria", name: "speech", value: "" },
])
createNewEntityClass_Auto("market", false, 39, 39, 1, 1, 0, 0, 1, 1, [
	{ type: "text", name: "item id", value: "coin", displayColor: "black", title: "Id предмета", optionsHint: ["coin", "heart"] },
	{ type: "number", name: "price", value: 1, displayColor: "black", title: "Цена" },
	{ type: "text", name: "market id", value: null, displayColor: "black", nullable: true, title: "Id магазина" },
	{ type: "textAria", name: "on buy speech", value: null, nullable: true, title: "Речь при покупке" },
	{ type: "textAria", name: "speech", value: null, nullable: true, title: "Рекламная речь" },
	{ type: "bool", name: "infinite", value: false, displayColor: "black", title: "Бесконечный товар" },
])
createNewEntityClass_Auto("trigger", false, 50, 50, 1, 1, 0, 0, 1, 1, [
	{ type: "area", name: "zone", value: [0, 0, 1, 1], displayColor: "orange", title: "Область активации" },
	{ type: "text", name: "type", value: "travelToWorld", displayColor: "green", options: ["travelToWorld", "dialog", "checkpoint"], title: "Тип" },
	{ type: "text", name: "value", value: null, displayColor: "lime", nullable: true, smartTitle: {
		field: "type",
		titles: { "travelToWorld": "Id Мира", "dialog": "Id диалога", "checkpoint": "Не используется" }
	}},
	{ type: "coords", name: "value2", value: null, displayColor: "lime", nullable: true, smartTitle: {
		field: "type",
		titles: { "travelToWorld": "Экран", "dialog": "Не используется", "checkpoint": "Не используется" }
	}},
	{ type: "tile", name: "value3", value: null, displayColor: "lime", nullable: true, smartTitle: {
		field: "type",
		titles: { "travelToWorld": "Место", "dialog": "Не используется", "checkpoint": "Точка возрождения" }
	}},
])
createNewEntityClass_Auto("cactusDancing", true, 18, 24, 0.85, 0.85, -0.075, -0.475, 1, 1.33)
const Aborigine = createNewEntityClass_Auto("aborigine", true, 15, 16, 0.32, 0.7, -0.241, -0.6, 1.2, 1.3, [
	{ type: "text", name: "type", value: "stay", options: ["stay", "patrol"] },
	{ type: "bool", name: "rotate", value: false, smartTitle: {
		field: "type",
		titles: { "stay": "Поворачивается ли", "patrol": "В конце пути идёт в начало" }
	}},
	{ type: "text", name: "direction", value: null, nullable: true, options: ["right", "down", "left", "up"], smartTitle: {
		field: "type",
		titles: { "stay": "Направление взгляда", "patrol": "Не используется" }
	}},
	{ type: "tilesNumered", name: "path", value: null, nullable: true, displayColor: "lime", smartTitle: {
		field: "type",
		titles: { "stay": "Не используется", "patrol": "Точки пути" }
	}},
])
const AborigineBow = createNewEntityClass_Auto("aborigineBow", true, 15, 16, 0.32, 0.7, -0.4, -0.6, 1.2, 1.3, [
	{ type: "text", name: "direction", value: "right", options: ["right", "down", "left", "up"], title: "Направление взгляда" },
])
createNewEntityClass_Auto("skeleton", true, 9, 13, 0.4, 0.55, -0.15, -0.45, 0.69, 1, [
	{ type: "text", name: "moveStyle", value: "ver", options: ["ver", "hor"], title: "Направление сдвига" },
	{ type: "bool", name: "dirR", value: true, smartTitle: {
		field: "moveStyle",
		titles: { "ver": "Вправо", "hor": "Вверх" },
	}, header: "Стартовое направление" },
	{ type: "bool", name: "rise", value: true, smartTitle: {
		field: "moveStyle",
		titles: { "ver": "Сдвиг вверх", "hor": "Сдвиг вправо" },
	} },
])
// createNewEntityClass_Auto("skeletonShield", true, 9, 13, 0.69, 1)
createNewEntityClass_Auto("tentacle", true, 16, 16, 0.5, 0.9375, -0.25, -0.0625, 1, 1, [
	{ type: "tiles", name: "appearCells", value: null, title: "Места появления", nullable: true, displayColor: "orange" },
])
createNewEntityClass_Auto("piranha", true, 16, 16, 0.9, 0.5, 0, -0.4375, 1, 1, [
	{ type: "text", name: "moveStyle", value: "ver", options: ["ver", "hor"], title: "Направление сдвига" },
	{ type: "bool", name: "dirR", value: true, smartTitle: {
		field: "moveStyle",
		titles: { "ver": "Вправо", "hor": "Вверх" },
	}, header: "Стартовое направление" },
	{ type: "bool", name: "rise", value: true, smartTitle: {
		field: "moveStyle",
		titles: { "ver": "Сдвиг вверх", "hor": "Сдвиг вправо" },
	} },
])
createNewEntityClass_Auto("cactusDancingChild", true, 18, 24, 0.85, 0.85, -0.075, -0.475, 1, 1.33, [
	{ type: "number", name: "color", value: 1, displayColor: "lime", options: [1, 2, 3, 4], title: "Цвет" },
])
createNewEntityClass_Auto("bush", false, 16, 16, 1, 1)
createNewEntityClass_Auto("wood", false, 14, 7, 0.875, 0.25, 0, -0.1875, 0.875, 0.4375)
createNewEntityClass_Auto("wood2", false, 15, 10, 0.6875, 0.625, -0.125, 0, 0.9375, 0.625)
createNewEntityClass_Auto("stone", true, 16, 16, 1, 1)
createNewEntityClass_Auto("stoneBar", false, 16, 16, 1, 1)
createNewEntityClass_Auto("lavaBubble", true, 16, 16, 0.5625, 0.5, -0.25, -0.25, 1, 1)
createNewEntityClass_Auto("octopus", true, 32, 32, 2, 2, undefined, undefined, undefined, undefined, [
	{ type: "area", name: "startZone", value: [2, 2, 16, 5], title: "Зона старта боя", displayColor: "orange" },
	{ type: "tiles", name: "entrance", value: [[19, 3], [19, 4], [19, 5]], title: "Вход", displayColor: "lime" },
	{ type: "tiles", name: "exit", value: [[0, 3], [0, 4], [0, 5]], title: "Выход", displayColor: "tomato" },
])
createNewEntityClass_Auto("spyglass", false, 11, 4, 0.6875, 0.25)
createNewEntityClass_Auto("dig_place_hidden", false, 16, 16, 1, 1, undefined, undefined, undefined, undefined, [
	{ type: "text", name: "content", value: "heart_add", options: ["heart_add"], title: "Содержимое" },
])
createNewEntityClass_Auto("pirate3", true, 11, 22, 0.75, 0.7, 0, -0.8, 0.75, 1.5, [
	{ type: "textAria", name: "speech", value: "", title: "Речь" },
	{ type: "number", name: "img", value: 1, options: [1, 2], title: "Изображение" },
])
createNewEntityClass_Auto("coinbag", null, 15, 12, 0.9375, 0.75, undefined, undefined, undefined, undefined, [
	{ type: "number", name: "id", value: 1, options: [1, 2, 3], title: "Id", displayColor: "green" },
])


function aborigineDraw(dirV: number, check0: boolean, lookR: number, lookW: number, maxR: number)
{
	function draw(self: Entity, ctx: CanvasRenderingContext2D)
	{
		let dir = 0;
		if (self.objData[0].value == "stay" || !check0)
		{
			switch (self.objData[dirV].value)
			{
				case "right": dir = 0; break;
				case "down": dir = Math.PI / 2; break;
				case "left": dir = Math.PI; break;
				case "up": dir = Math.PI / 2 * 3; break;
			}
		}
		else
		{
			const tiles = self.objData[3].value;
			if (tiles && tiles[1])
			{
				const dx = tiles[1][0] - Math.floor(self.x);
				const dy = tiles[1][1] - Math.floor(self.y);
				if (dx > 0) dir = 0;
				else if (dx < 0) dir = Math.PI;
				else if (dy > 0) dir = Math.PI / 2;
				else if (dy < 0) dir = Math.PI / 2 * 3;
			}
		}
		const drawPie = (r: number, w: number, d: number) =>
		{
			ctx.beginPath();
			ctx.moveTo(self.x * TileSize, self.y * TileSize);
			ctx.arc(self.x * TileSize, self.y * TileSize, r * TileSize, d - w / 2, d + w / 2)
			ctx.lineTo(self.x * TileSize, self.y * TileSize);
			ctx.fill();
		}
		ctx.save();
		if (self.objData[0].value == "stay" || !check0)
		{
			ctx.fillStyle = "rgba(128, 128, 128, 0.2)";
			const addW = !check0 || self.objData[1].value ? maxR / 180 * Math.PI : 20 / 180 * Math.PI
			drawPie(lookR, addW, dir + lookW / 2 + addW / 2);
			drawPie(lookR, addW, dir - lookW / 2 - addW / 2);
		}
		ctx.fillStyle = "rgba(255, 165, 0, 0.2)";
		drawPie(lookR, lookW, dir);
		ctx.restore();
	}
	return draw;
}
Aborigine.customDraw = aborigineDraw(2, true, 4, Math.PI / 2, 60);
AborigineBow.customDraw = aborigineDraw(0, false, 7.5, Math.PI / 3 * 2, 40);