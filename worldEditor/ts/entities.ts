// name, imgUrl, width, height, widthHitbox, heightHitbox, xImg, yImg, widthImg, heightImg, objData

createNewEntityClass_Auto("crab-kolobok", false, 13, 11, 0.8, 0.677, 0, 0, 0.8, 0.677, [
	{ type: "bool", name: "sleeping", value: true },
	{ type: "number", name: "hp", value: 1, displayColor: "black" },
	{ type: "text", name: "tag", value: null, displayColor: "black" },
	{ type: "aura", name: "atackArea", value: { x: 0.5, y: 0.5, w: 1, h: 1 }, displayColor: "orange" },
	{ type: "area", name: "sleepArea", value: { x: 6, y: 2, w: 5, h: 3 }, displayColor: "azure" },
	{ type: "tile", name: "favoriteTile", value: { x: 1, y: 4 }, displayColor: "pink" },
	{ type: "tiles", name: "killingTiles", value: [{ x: 13, y: 2 }, { x: 13, y: 3 }], displayColor: "tomato" },
]);

createNewEntityClass_Auto("crab", true, 20, 11, 1, 0.55)
createNewEntityClass_Auto("cactus", false, 16, 16, 0.85, 0.85, -0.075, -0.075, 1, 1)
createNewEntityClass_Auto("door", false, 11, 12, 1, 1)
createNewEntityClass_Auto("palm", false, 20, 22, 0.45, 0.7, -0.45, -0.8, 1.5, 1.5)
createNewEntityClass_Auto("trader", true, 14, 24, 0.75, 0.7, 0, -0.8, 0.75, 1.5)
createNewEntityClass_Auto("cannon", true, 11, 12, 1, 1)
createNewEntityClass_Auto("trainer", false, 9, 18, 0.75, 0.7, 0, -0.8, 0.75, 1.5)
createNewEntityClass_Auto("pirate2", true, 11, 22, 0.75, 0.7, 0, -0.8, 0.75, 1.5, [
	{ type: "text", name: "speech", value: "" },
])
