from __future__ import annotations
import math
from time import time as curTime
import pygame
from functions import GameExeption, load_tile
from settings import Settings


class Tile:
    tileIds: dict[str, Tile] = {}

    def __init__(self, image: str, solid: bool = False, digable: bool = False, speed: float = 1, tags=None, damage: int = 0):
        self.image = load_tile(image)
        self.image = pygame.transform.scale(self.image, (Settings.tileSize, Settings.tileSize))
        self.speed = speed  # множитель скорости клетки
        self.digable = digable  # можно ли копать на этой клетке
        self.solid = solid  # плотная ли клетка (стена)
        self._damage = damage  # урон при наступании на клетку
        self.id = image[:image.index(".")]
        self.tags = []
        if (tags):
            self.tags = tags
        Tile.tileIds[self.id] = self

    @staticmethod
    def fromId(id: str) -> Tile:
        if (id in Tile.tileIds):
            return Tile.tileIds[id]
        raise GameExeption(f"Tile.fromId: no tile with id: {id}")

    def draw(self, surface: pygame.Surface, x: int, y: int):
        surface.blit(self.image, (x * Settings.tileSize, y * Settings.tileSize))

    def damage(self, x: int, y: int):
        return self._damage


class TileAnimated(Tile):
    def __init__(self, image: str, solid: bool = False, digable: bool = False, speed: float = 1, tags=None, damage: int = 0, tileSize=16, animSpeed=100):
        super().__init__(image, solid, digable, speed, tags, damage)
        img = load_tile(image)
        self.frames = []
        count = img.get_width() // tileSize
        for x in range(count):
            frame = img.subsurface(x * tileSize, 0, tileSize, tileSize)
            frame = pygame.transform.scale(frame, (Settings.tileSize, Settings.tileSize))
            self.frames.append(frame)
        self.image = self.frames[0]
        self.animlen = len(self.frames)
        self.a_damage = [0 for _ in range(self.animlen)]
        self.a_speed = [animSpeed for _ in range(self.animlen)]
        self.animDur = sum(self.a_speed)
        self.delayX = 0
        self.delayY = 0

    def getFrame(self, x: int, y: int):
        timeNow = curTime() * 1000 + x * self.delayX + y * self.delayY
        time = (math.floor(timeNow) + self.animDur) % self.animDur
        t = 0
        for i, spd in enumerate(self.a_speed):
            t += spd
            if (time <= t):
                return i
        return self.animlen - 1

    def draw(self, surface: pygame.Surface, x: int, y: int):
        frame = self.getFrame(x, y)
        self.image = self.frames[frame]
        super().draw(surface, x, y)

    def damage(self, x: int, y: int):
        frame = self.getFrame(x, y)
        if (len(self.a_damage) <= frame):
            return 0
        return self.a_damage[frame]

    def s_dmg(self, damage: list[int]):
        for i, dmg in enumerate(damage):
            self.a_damage[i] = dmg
        return self

    def s_dmgD(self, damage: dict[int, int]):
        for key in damage:
            self.a_damage[key] = damage[key]
        return self

    def s_dmgL(self, indexes: list[int], damage: int):
        for i in indexes:
            self.a_damage[i] = damage
        return self

    def s_spd(self, speed: list[int]):
        for i, spd in enumerate(speed):
            self.a_speed[i] = spd
        self.animDur = sum(self.a_speed)
        return self

    def s_spdD(self, speed: dict[int, int]):
        for key in speed:
            self.a_speed[key] = speed[key]
        self.animDur = sum(self.a_speed)
        return self

    def s_spdL(self, indexes: list[int], speed: int):
        for i in indexes:
            self.a_speed[i] = speed
        return self

    def s_del(self, x: int, y: int):
        self.delayX = x
        self.delayY = y
        return self


Tile("sand1.png", digable=True, tags=["sand"])
Tile("sand2.png", digable=True, tags=["sand"])
Tile("sand3.png", digable=True, tags=["sand"])
Tile("grass1.png")
Tile("grass2.png")
Tile("grass3.png")
Tile("stone.png")

Tile("water_deep.png", solid=True)
Tile("water_low.png", speed=0.6, tags=["water"])

Tile("mountain.png", solid=True)
Tile("mountain2.png", solid=True)
Tile("mountain_sand.png", solid=True)
Tile("mountain_sand2.png", solid=True)

Tile("A.png", digable=True)
Tile("D.png", digable=True)
Tile("S.png", digable=True)
Tile("W.png", digable=True)
Tile("AttackB.png", digable=True)
Tile("DigB.png", digable=True)

Tile("water_sand_t.png", speed=0.6, tags=["water", "water-t"])
Tile("water_sand_r.png", speed=0.6, tags=["water", "water-r"])
Tile("water_sand_b.png", speed=0.6, tags=["water", "water-b"])
Tile("water_sand_l.png", speed=0.6, tags=["water", "water-l"])
Tile("water_sand_tl.png", speed=0.6, tags=["water", "water-t", "water-l"])
Tile("water_sand_tr.png", speed=0.6, tags=["water", "water-t", "water-r"])
Tile("water_sand_bl.png", speed=0.6, tags=["water", "water-b", "water-l"])
Tile("water_sand_br.png", speed=0.6, tags=["water", "water-b", "water-r"])
Tile("water_sand_tbl.png", speed=0.6, tags=["water", "water-t", "water-b", "water-l"])
Tile("water_sand_tbr.png", speed=0.6, tags=["water", "water-t", "water-b", "water-r"])
Tile("water_sand_tlr.png", speed=0.6, tags=["water", "water-t", "water-l", "water-r"])
Tile("water_sand_blr.png", speed=0.6, tags=["water", "water-b", "water-l", "water-r"])
Tile("water_sand_tl2.png", speed=0.6, tags=["water"])
Tile("water_sand_tr2.png", speed=0.6, tags=["water"])
Tile("water_sand_bl2.png", speed=0.6, tags=["water"])
Tile("water_sand_br2.png", speed=0.6, tags=["water"])
Tile("water_sand_tl_bl.png", speed=0.6, tags=["water"])
Tile("water_sand_tl_tr.png", speed=0.6, tags=["water"])
Tile("water_sand_tr_br.png", speed=0.6, tags=["water"])
Tile("water_sand_bl_br.png", speed=0.6, tags=["water"])

Tile("water_deep_sand_t.png", solid=True)
Tile("water_deep_sand_r.png", solid=True)
Tile("water_deep_sand_b.png", solid=True)
Tile("water_deep_sand_l.png", solid=True)
Tile("water_deep_sand_tl.png", solid=True)
Tile("water_deep_sand_tr.png", solid=True)
Tile("water_deep_sand_bl.png", solid=True)
Tile("water_deep_sand_br.png", solid=True)
Tile("water_deep_sand_tbl.png", solid=True)
Tile("water_deep_sand_tbr.png", solid=True)
Tile("water_deep_sand_tlr.png", solid=True)
Tile("water_deep_sand_blr.png", solid=True)
Tile("water_deep_sand_tl2.png", solid=True)
Tile("water_deep_sand_tr2.png", solid=True)
Tile("water_deep_sand_bl2.png", solid=True)
Tile("water_deep_sand_br2.png", solid=True)
Tile("water_deep_sand_tl_bl.png", solid=True)
Tile("water_deep_sand_tl_tr.png", solid=True)
Tile("water_deep_sand_tr_br.png", solid=True)
Tile("water_deep_sand_bl_br.png", solid=True)

Tile("grass_sand_t.png")
Tile("grass_sand_r.png")
Tile("grass_sand_b.png")
Tile("grass_sand_l.png")
Tile("grass_sand_tl.png")
Tile("grass_sand_tr.png")
Tile("grass_sand_bl.png")
Tile("grass_sand_br.png")
Tile("grass_sand_tbl.png")
Tile("grass_sand_tbr.png")
Tile("grass_sand_tlr.png")
Tile("grass_sand_blr.png")
Tile("grass_sand_tl2.png")
Tile("grass_sand_tr2.png")
Tile("grass_sand_bl2.png")
Tile("grass_sand_br2.png")
Tile("grass_sand_tl_bl.png")
Tile("grass_sand_tl_tr.png")
Tile("grass_sand_tr_br.png")
Tile("grass_sand_bl_br.png")

Tile("lava.png")
Tile("lavaAct.png", damage=1)
TileAnimated("lavaAnim.png", animSpeed=200) \
    .s_dmgL([4, 5, 6], 1) \
    .s_del(-50, 0) \
    .s_spdD({0: 4000, 5: 2000})
