"use strict";
// name, imgUrl, width, height, widthHitbox, heightHitbox, xImg, yImg, widthImg, heightImg, objData
createNewEntityClass_Auto("crab", false, 13, 11, 0.8, 0.677, 0, 0, 0.8, 0.677, [
    { type: "bool", name: "sleeping", value: true },
    { type: "number", name: "hp", value: 1, displayColor: "black" },
    { type: "text", name: "tag", value: null, displayColor: "black" },
    { type: "aura", name: "atackArea", value: { x: 0.5, y: 0.5, w: 1, h: 1 }, displayColor: "orange" },
    { type: "area", name: "sleepArea", value: { x: 6, y: 2, w: 5, h: 3 }, displayColor: "azure" },
    { type: "tile", name: "favoriteTile", value: { x: 1, y: 4 }, displayColor: "pink" },
    { type: "tiles", name: "killingTiles", value: [{ x: 13, y: 2 }, { x: 13, y: 3 }], displayColor: "tomato" },
]);
createNewEntityClass_Auto("cactus", false, 16, 16, 1, 1);
createNewEntityClass_Auto("door", false, 11, 12, 1, 1);
createNewEntityClass_Auto("palm", false, 20, 22, 1, 1);
createNewEntityClass_Auto("trader", true, 14, 24, 0.75, 1, 0, -0.5, 0.75, 1.5);
createNewEntityClass_Auto("cannon", true, 11, 12, 1, 1);
