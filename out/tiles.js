"use strict";
const tileIds = {
    water_deep: "water_deep.png",
    water_low: "water_low.png",
    stone: "stone.png",
};
const tileList = [];
// Название группы должно совпадать с названием одного из тайлов, этот тайл будет использоваться для обложки
const tileGroups = {
    mountain: {
        tiles: {
            mountain: "mountain.png",
            mountain2: "mountain2.png",
            mountain_sand: "mountain_sand.png",
            mountain_sand2: "mountain_sand2.png",
        },
        random: false
    },
    sand1: {
        tiles: {
            sand1: "sand1.png",
            sand2: "sand2.png",
            sand3: "sand3.png",
        },
        random: true
    },
    grass1: {
        tiles: {
            grass1: "grass1.png",
            grass2: "grass2.png",
            grass3: "grass3.png",
        },
        random: true
    },
    AttackB: {
        tiles: {
            A: "A.png",
            AttackB: "AttackB.png",
            D: "D.png",
            DigB: "DigB.png",
            S: "S.png",
            W: "W.png",
        },
        random: false
    },
    lava: {
        tiles: {
            lava: "lava.png",
            lavaAct: "lavaAct.png",
            lavaAnim: "/lava.png",
        },
        random: false
    }
};
for (const key in tileIds)
    tileList.push({ key, group: false, random: false });
for (const key in tileGroups) {
    const el = tileGroups[key];
    tileList.push({ key, group: true, random: el.random });
    const group = el.tiles;
    for (const key in group) {
        tileIds[key] = group[key];
    }
}
