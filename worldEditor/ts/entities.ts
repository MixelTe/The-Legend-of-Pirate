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
createNewEntityClass_Auto("aborigine", true, 15, 16, 0.93, 1)
createNewEntityClass_Auto("aborigineBow", true, 15, 16, 0.93, 1)
createNewEntityClass_Auto("skeleton", true, 9, 13, 0.4, 0.55, -0.15, -0.45, 0.69, 1, [
	{ type: "text", name: "direction", value: "right", options: ["right", "left"], title: "Направление" },
	{ type: "bool", name: "rise", value: true, title: "Поднимается ли" },
])
createNewEntityClass_Auto("skeletonShield", true, 9, 13, 0.69, 1)
createNewEntityClass_Auto("tentacle", true, 28, 34, 0.82, 1)
createNewEntityClass_Auto("piranha", true, 35, 32, 1, 0.91)
createNewEntityClass_Auto("cactusDancingChild", true, 18, 24, 0.85, 0.85, -0.075, -0.475, 1, 1.33, [
	{ type: "number", name: "color", value: 1, displayColor: "lime", options: [1, 2, 3, 4], title: "Цвет" },
])
