from __future__ import annotations
import pygame
from functions import GameExeption, load_tile
from settings import Settings


class Tile:
    tileIds: dict[str, Tile] = {}

    def __init__(self, image: str, solid: bool = False, digable: bool = False, speed: float = 1, tags=None):
        self.image = load_tile(image)
        self.image = pygame.transform.scale(self.image, (int(Settings.tileSize), int(Settings.tileSize)))
        self.speed = speed  # множитель скорости клетки
        self.digable = digable  # можно ли копать на этой клетке
        self.solid = solid  # плотная ли клетка (стена)
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


Tile("sand1.png", digable=True, tags=["sand"])
Tile("sand2.png", digable=True, tags=["sand"])
Tile("sand3.png", digable=True, tags=["sand"])
Tile("grass1.png")
Tile("grass2.png")
Tile("grass3.png")
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
Tile("water_sand_tbl.png", speed=0.6, tags=["water", "water-t", "water-b","water-l"])
Tile("water_sand_tbr.png", speed=0.6, tags=["water", "water-t", "water-b","water-r"])
Tile("water_sand_tlr.png", speed=0.6, tags=["water", "water-t", "water-l","water-r"])
Tile("water_sand_blr.png", speed=0.6, tags=["water", "water-b", "water-l","water-r"])
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
