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
createNewEntityClass_Auto("dig_place", false, 7, 7, 1, 1, 0.35, 0.35, 0.3, 0.3)
createNewEntityClass_Auto("trainer", true, 9, 18, 0.75, 0.7, 0, -0.8, 0.75, 1.5)
createNewEntityClass_Auto("pirate2", true, 11, 22, 0.75, 0.7, 0, -0.8, 0.75, 1.5, [
	{ type: "textAria", name: "speech", value: "" },
])
createNewEntityClass_Auto("market", false, 39, 39, 1, 1, 0, 0, 1, 1, [
	{ type: "text", name: "item id", value: "coin", displayColor: "black", title: "Id предмета" },
	{ type: "number", name: "price", value: 1, displayColor: "lime", title: "Цена" },
	{ type: "text", name: "market id", value: null, displayColor: "lime", nullable: true, title: "Id магазина" },
	{ type: "textAria", name: "on buy speech", value: null, nullable: true, title: "Речь при покупке" },
	{ type: "textAria", name: "speech", value: null, nullable: true, title: "Рекламная речь" },
])
createNewEntityClass_Auto("trigger", false, 50, 50, 1, 1, 0, 0, 1, 1, [
	{ type: "area", name: "zone", value: [0, 0, 1, 1], displayColor: "orange", title: "Область активации" },
	{ type: "text", name: "type", value: "travelToWorld", displayColor: "lime", options: ["travelToWorld", "dialog"], title: "Тип" },
	{ type: "text", name: "value", value: null, displayColor: "lime", nullable: true, smartTitle: {
		field: "type",
		titles: { "travelToWorld": "Id Мира", "dialog": "Id диалога" }
	}},
	{ type: "coords", name: "value2", value: null, displayColor: "lime", nullable: true, smartTitle: {
		field: "type",
		titles: { "travelToWorld": "Экран", "dialog": "Не используется" }
	}},
	{ type: "tile", name: "value3", value: null, displayColor: "lime", nullable: true, smartTitle: {
		field: "type",
		titles: { "travelToWorld": "Место", "dialog": "Не используется" }
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
		titles: { "stay": "Напривление взгляда", "patrol": "Не используется" }
	}},
	{ type: "tilesNumered", name: "path", value: null, nullable: true, displayColor: "lime", smartTitle: {
		field: "type",
		titles: { "stay": "Не используется", "patrol": "Точки пути" }
	}},
])
createNewEntityClass_Auto("aborigineBow", true, 15, 16, 0.32, 0.7, -0.241, -0.6, 1.2, 1.3)
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
createNewEntityClass_Auto("tentacle", true, 28, 34, 0.82, 1)
createNewEntityClass_Auto("piranha", true, 35, 32, 0.8, 0.7, -0.05, -0.15, 1, 0.91, [
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
createNewEntityClass_Auto("stone", false, 16, 16, 1, 1)
createNewEntityClass_Auto("stoneBar", false, 16, 16, 1, 1)
createNewEntityClass_Auto("lavaBubble", true, 51, 56, 1, 1)


Aborigine.customDraw = (self, ctx) =>
{
	const lookR = 4;
	let lookW = Math.PI / 2
	let dir = 0;
	if (self.objData[0].value == "stay")
	{
		switch (self.objData[2].value)
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
	if (self.objData[0].value == "stay")
	{
		ctx.fillStyle = "rgba(128, 128, 128, 0.2)";
		const addW = self.objData[1].value ? 60 / 180 * Math.PI : 20 / 180 * Math.PI
		drawPie(lookR, addW, dir + lookW / 2 + addW / 2);
		drawPie(lookR, addW, dir - lookW / 2 - addW / 2);
	}
	ctx.fillStyle = "rgba(255, 165, 0, 0.2)";
	drawPie(lookR, lookW, dir);
	ctx.restore();
};