"use strict";
// name, imgUrl, width, height, widthHitbox, heightHitbox, xImg, yImg, widthImg, heightImg, objData
createNewEntityClass_Auto("crab-kolobok", false, 13, 11, 0.8, 0.677, 0, 0, 0.8, 0.677, [
    { type: "bool", name: "sleeping", value: true },
    { type: "number", name: "hp", value: 1, displayColor: "black" },
    { type: "text", name: "tag", value: null, displayColor: "black" },
    { type: "aura", name: "atackArea", value: [0.5, 0.5, 1, 1], displayColor: "orange" },
    { type: "area", name: "sleepArea", value: [6, 2, 5, 3], displayColor: "azure" },
    { type: "tile", name: "favoriteTile", value: [1, 4], displayColor: "pink" },
    { type: "tiles", name: "killingTiles", value: [[13, 2], [13, 3]], displayColor: "tomato" },
]);
createNewEntityClass_Auto("crab", true, 20, 11, 1, 0.55);
createNewEntityClass_Auto("cactus", false, 16, 16, 0.85, 0.85, -0.075, -0.075, 1, 1);
createNewEntityClass_Auto("door", false, 11, 12, 1, 1);
createNewEntityClass_Auto("palm", false, 20, 22, 0.45, 0.7, -0.45, -0.8, 1.5, 1.5);
createNewEntityClass_Auto("trader", true, 14, 24, 0.75, 0.7, 0, -0.8, 0.75, 1.5);
createNewEntityClass_Auto("cannon", true, 11, 12, 1, 1);
createNewEntityClass_Auto("dig_place", false, 11, 12, 1, 1);
createNewEntityClass_Auto("trainer", true, 9, 18, 0.75, 0.7, 0, -0.8, 0.75, 1.5);
createNewEntityClass_Auto("pirate2", true, 11, 22, 0.75, 0.7, 0, -0.8, 0.75, 1.5, [
    { type: "text", name: "speech", value: "" },
]);
createNewEntityClass_Auto("market", false, 39, 39, 1, 1, 0, 0, 1, 1, [
    { type: "text", name: "item id", value: "coin", displayColor: "black" },
    { type: "number", name: "price", value: 1, displayColor: "lime" },
    { type: "text", name: "market id", value: null, displayColor: "lime" },
    { type: "text", name: "on buy speech", value: null },
    { type: "text", name: "speech", value: null },
]);
createNewEntityClass_Auto("trigger", false, 50, 50, 1, 1, 0, 0, 1, 1, [
    { type: "text", name: "dialog", value: null, displayColor: "lime" },
    { type: "area", name: "zone", value: null, displayColor: "orange" },
]);
createNewEntityClass_Auto("cactusDancing", true, 18, 24, 0.85, 0.85, -0.075, -0.475, 1, 1.33);
