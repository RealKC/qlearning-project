from typing import Literal, Union
import pygame
from abc import ABC, abstractmethod
from pygame import Surface

SIZE = 128

Coordinate = tuple[float, float]

class Tile(ABC):
    coord: Coordinate

    def __init__(self, coord: Coordinate):
        self.coord = coord

    def draw(self, bg: Surface):
        pass

class TileMap:
    tiles: list[list[Tile]]

    def __init__(self, tiles: list[list[Tile]]):
        self.tiles = tiles

    def draw(self, bg: Surface):
        for line in self.tiles:
            for tile in line:
                tile.draw(bg)

def render_map(map: str) -> TileMap:
    lines = map.splitlines()
    res = []

    for (i, line) in enumerate(lines):
        l = []
        for (j, ch) in enumerate(line):
            coord = (i * SIZE, j * SIZE)
            match ch:
                case '0': l.append(Tile(coord))
                case '1': l.append(StraightLine(coord, "horizontal"))
                case '2': l.append(StraightLine(coord, "vertical"))
                case '3': l.append(Diagonal(coord, 0))
                case '4': l.append(Diagonal(coord, 90))
                case '5': l.append(Diagonal(coord, 180))
                case '6': l.append(Diagonal(coord, 270))
        res.append(l)

    return TileMap(res)


Direction = Literal["vertical", "horizontal"]

class StraightLine(Tile):
    direction: Direction

    def __init__(self, coord: Coordinate, direction: Direction = "vertical"):
        super().__init__(coord)
        self.direction = direction

    def draw(self, bg: Surface):
        tile = Surface((SIZE, SIZE))

        tile.fill("white")
        pygame.draw.line(tile, "black", (0, 0), (0, SIZE), 6)
        pygame.draw.line(tile, "black", (SIZE, 0), (SIZE, SIZE), 6)

        if self.direction == "horizontal":
            tile = pygame.transform.rotate(tile, 90)

        bg.blit(tile, self.coord)

class Diagonal(Tile):
    angle: float

    def __init__(self, coord: Coordinate, angle: float):
        super().__init__(coord)
        self.angle = angle

    def draw(self, bg: Surface):
        tile = Surface((SIZE, SIZE), pygame.SRCALPHA)

        tile.fill("white")
        pygame.draw.line(tile, "black", (0, SIZE), (SIZE, 0), 4)
        tile = pygame.transform.rotate(tile, self.angle)

        bg.blit(tile, self.coord)
