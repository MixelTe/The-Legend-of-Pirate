from __future__ import annotations
import pygame
from functions import GameExeption, load_tile
from settings import Settings


class Tile:
    tileIds: dict[str, Tile] = {}
    def __init__(self, image: str, solid: bool = False, digable: bool = False, speed: float = 1, tags=None):
        self.image = load_tile(image)
        self.image = pygame.transform.scale(self.image, (Settings.tileSize, Settings.tileSize))
        self.speed = speed # множитель скорости клетки
        self.digable = digable # можно ли копать на этой клетке
        self.solid = solid # плотная ли клетка (стена)
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


Tile("sand1.png", digable=True)
Tile("sand2.png", digable=True)
Tile("sand3.png", digable=True)
Tile("grass1.png")
Tile("grass2.png")
Tile("grass3.png")
Tile("water_deep.png", solid=True)
Tile("water_low.png", speed=0.6, tags=["water"])
Tile("mountain.png", solid=True)
Tile("mountain2.png", solid=True)
Tile("mountain_sand.png", solid=True)
Tile("mountain_sand2.png", solid=True)
Tile("A.png")
Tile("D.png")
Tile("S.png")
Tile("W.png")
Tile("AttackB.png")
Tile("DigB.png")

Tile("water_sand_t.png", speed=0.6)
Tile("water_sand_r.png", speed=0.6)
Tile("water_sand_b.png", speed=0.6)
Tile("water_sand_l.png", speed=0.6)
Tile("water_sand_tl.png", speed=0.6)
Tile("water_sand_tr.png", speed=0.6)
Tile("water_sand_bl.png", speed=0.6)
Tile("water_sand_br.png", speed=0.6)
Tile("water_sand_tbl.png", speed=0.6)
Tile("water_sand_tbr.png", speed=0.6)
Tile("water_sand_tlr.png", speed=0.6)
Tile("water_sand_blr.png", speed=0.6)
Tile("water_sand_tl2.png", speed=0.6)
Tile("water_sand_tr2.png", speed=0.6)
Tile("water_sand_bl2.png", speed=0.6)
Tile("water_sand_br2.png", speed=0.6)
Tile("water_sand_tl_tl.png", speed=0.6)
Tile("water_sand_tl_tr.png", speed=0.6)
Tile("water_sand_tr_br.png", speed=0.6)
Tile("water_sand_bl_br.png", speed=0.6)

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
Tile("water_deep_sand_tl_tl.png", solid=True)
Tile("water_deep_sand_tl_tr.png", solid=True)
Tile("water_deep_sand_tr_br.png", solid=True)
Tile("water_deep_sand_bl_br.png", solid=True)