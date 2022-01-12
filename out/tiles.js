"use strict";
const tileIds = {
    water_deep: "water_deep.png",
    water_low: "water_low.png",
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
    water_sand_t: {
        tiles: {
            water_sand_t: "water_sand_t.png",
            water_sand_r: "water_sand_r.png",
            water_sand_b: "water_sand_b.png",
            water_sand_l: "water_sand_l.png",
            water_sand_tl: "water_sand_tl.png",
            water_sand_tr: "water_sand_tr.png",
            water_sand_bl: "water_sand_bl.png",
            water_sand_br: "water_sand_br.png",
            water_sand_tbl: "water_sand_tbl.png",
            water_sand_tbr: "water_sand_tbr.png",
            water_sand_tlr: "water_sand_tlr.png",
            water_sand_blr: "water_sand_blr.png",
            water_sand_tl2: "water_sand_tl2.png",
            water_sand_tr2: "water_sand_tr2.png",
            water_sand_bl2: "water_sand_bl2.png",
            water_sand_br2: "water_sand_br2.png",
            water_sand_tl_bl: "water_sand_tl_bl.png",
            water_sand_tl_tr: "water_sand_tl_tr.png",
            water_sand_tr_br: "water_sand_tr_br.png",
            water_sand_bl_br: "water_sand_bl_br.png",
            water_sand_tl_br: "water_sand_tl_br.png",
            water_sand_tr_bl: "water_sand_tr_bl.png",
        },
        random: false
    },
    water_deep_sand_t: {
        tiles: {
            water_deep_sand_t: "water_deep_sand_t.png",
            water_deep_sand_r: "water_deep_sand_r.png",
            water_deep_sand_b: "water_deep_sand_b.png",
            water_deep_sand_l: "water_deep_sand_l.png",
            water_deep_sand_tl: "water_deep_sand_tl.png",
            water_deep_sand_tr: "water_deep_sand_tr.png",
            water_deep_sand_bl: "water_deep_sand_bl.png",
            water_deep_sand_br: "water_deep_sand_br.png",
            water_deep_sand_tbl: "water_deep_sand_tbl.png",
            water_deep_sand_tbr: "water_deep_sand_tbr.png",
            water_deep_sand_tlr: "water_deep_sand_tlr.png",
            water_deep_sand_blr: "water_deep_sand_blr.png",
            water_deep_sand_tl2: "water_deep_sand_tl2.png",
            water_deep_sand_tr2: "water_deep_sand_tr2.png",
            water_deep_sand_bl2: "water_deep_sand_bl2.png",
            water_deep_sand_br2: "water_deep_sand_br2.png",
            water_deep_sand_tl_bl: "water_deep_sand_tl_bl.png",
            water_deep_sand_tl_tr: "water_deep_sand_tl_tr.png",
            water_deep_sand_tr_br: "water_deep_sand_tr_br.png",
            water_deep_sand_bl_br: "water_deep_sand_bl_br.png",
            water_deep_sand_tl_br: "water_deep_sand_tl_br.png",
            water_deep_sand_tr_bl: "water_deep_sand_tr_bl.png",
        },
        random: false
    },
    grass_sand_t: {
        tiles: {
            grass_sand_t: "grass_sand_t.png",
            grass_sand_r: "grass_sand_r.png",
            grass_sand_b: "grass_sand_b.png",
            grass_sand_l: "grass_sand_l.png",
            grass_sand_tl: "grass_sand_tl.png",
            grass_sand_tr: "grass_sand_tr.png",
            grass_sand_bl: "grass_sand_bl.png",
            grass_sand_br: "grass_sand_br.png",
            grass_sand_tbl: "grass_sand_tbl.png",
            grass_sand_tbr: "grass_sand_tbr.png",
            grass_sand_tlr: "grass_sand_tlr.png",
            grass_sand_blr: "grass_sand_blr.png",
            grass_sand_tl2: "grass_sand_tl2.png",
            grass_sand_tr2: "grass_sand_tr2.png",
            grass_sand_bl2: "grass_sand_bl2.png",
            grass_sand_br2: "grass_sand_br2.png",
            grass_sand_tl_bl: "grass_sand_tl_bl.png",
            grass_sand_tl_tr: "grass_sand_tl_tr.png",
            grass_sand_tr_br: "grass_sand_tr_br.png",
            grass_sand_bl_br: "grass_sand_bl_br.png",
            grass_sand_tl_br: "grass_sand_tl_br.png",
            grass_sand_tr_bl: "grass_sand_tr_bl.png",
        },
        random: false
    },
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
