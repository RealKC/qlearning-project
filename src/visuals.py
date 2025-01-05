from typing import Literal, get_args
import pygame
from abc import ABC
from pygame import Surface

SIZE = 128

Coordinate = tuple[float, float]

Direction = Literal["up", "right", "down", "left"]
directions = get_args(Direction)


class Tile(ABC):
    coord: Coordinate
    font: pygame.font.SysFont

    def __init__(self, coord: Coordinate):
        self.coord = coord
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), size=12)

    def draw(self, bg: Surface):
        pass

    def can_go_to(self, direction: Direction) -> bool:
        return False

    def _draw_allowed_directions(self, target: Surface):
        for dir in directions:
            if self.can_go_to(dir):
                text = self.font.render(dir, True, (0, 0, 0))
                match dir:
                    case "down":
                        target.blit(text, (SIZE / 2, SIZE - 20))
                        # pygame.draw.circle(tile, "blue", (SIZE / 2, 5), 5)
                    case "right":
                        target.blit(text, (SIZE - 20, SIZE / 2))
                        # pygame.draw.circle(tile, "blue", (SIZE - 5, SIZE / 2), 5)
                    case "left":
                        target.blit(text, (5, SIZE / 2))
                        # pygame.draw.circle(tile, "blue", (5, SIZE / 2), 5)
                    case "up":
                        target.blit(text, (SIZE / 2, 20))
                        # pygame.draw.circle(tile, "blue", (SIZE / 2, SIZE - 5), 5)


class TileMap:
    tiles: list[list[Tile]]
    agent: Coordinate
    goal: Coordinate

    def __init__(self, tiles: list[list[Tile]], goal: Coordinate, init: Coordinate):
        self.tiles = tiles
        self.goal = goal
        self.agent = init

    def is_goal(self, coord: Coordinate) -> bool:
        adjusted = (self.goal[0] * SIZE, self.goal[1] * SIZE)

        return coord[0] == adjusted[0] and coord[1] == adjusted[1]

    def draw(self, bg: Surface):
        for line in self.tiles:
            for tile in line:
                tile.draw(bg)

        goal = Surface((64, 64))
        goal.fill("yellow")

        bg.blit(goal, (self.goal[0] * SIZE + SIZE / 4, self.goal[1] * SIZE + SIZE / 4))

        goal.fill("red")
        bg.blit(
            goal, (self.agent[0] * SIZE + SIZE / 4, self.agent[1] * SIZE + SIZE / 4)
        )

    def move_agent(self, coord: Coordinate):
        # TODO: Animate this somehow

        self.agent = coord

    @property
    def width(self) -> float:
        return len(self.tiles[0])

    @property
    def height(self) -> float:
        return len(self.tiles)


def render_map(map: str, goal: Coordinate, init: Coordinate) -> TileMap:
    lines = map.splitlines()
    res = []

    for i, line in enumerate(lines):
        tile_line = []
        for j, ch in enumerate(line):
            coord = (i * SIZE, j * SIZE)
            match ch:
                case "0":
                    tile_line.append(Tile(coord))
                case "1":
                    tile_line.append(StraightLine(coord, "horizontal"))
                case "2":
                    tile_line.append(StraightLine(coord, "vertical"))
                case "3":
                    tile_line.append(Diagonal(coord, 0))
                case "4":
                    tile_line.append(Diagonal(coord, 90))
                case "5":
                    tile_line.append(Diagonal(coord, 180))
                case "6":
                    tile_line.append(Diagonal(coord, 270))
        res.append(tile_line)

    return TileMap(res, goal, init)


Orientation = Literal["vertical", "horizontal"]


class StraightLine(Tile):
    orientation: Orientation

    def __init__(self, coord: Coordinate, direction: Orientation = "vertical"):
        super().__init__(coord)
        self.orientation = direction

    def draw(self, bg: Surface):
        tile = Surface((SIZE, SIZE))

        tile.fill("white")
        pygame.draw.line(tile, "black", (0, 0), (0, SIZE), 6)
        pygame.draw.line(tile, "black", (SIZE, 0), (SIZE, SIZE), 6)

        if self.orientation == "horizontal":
            tile = pygame.transform.rotate(tile, 90)

        self._draw_allowed_directions(tile)
        orientation = self.font.render(self.orientation, True, (0, 0, 0))
        tile.blit(orientation, (SIZE / 2, SIZE / 2))

        bg.blit(tile, self.coord)

    def can_go_to(self, direction: Direction):
        if self.orientation == "vertical":
            return direction in ["up", "down"]

        return direction in ["right", "left"]


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

        font = pygame.font.SysFont(pygame.font.get_default_font(), size=12)
        self._draw_allowed_directions(tile)

        degrees = font.render(str(self.angle), True, (0, 0, 0))

        tile.blit(degrees, (SIZE / 2, SIZE / 2))

        bg.blit(tile, self.coord)

    def can_go_to(self, direction: Direction):
        match self.angle:
            case 0:
                return direction in ["down", "right"]
            case 90:
                return direction in ["up", "right"]
            case 180:
                return direction in ["up", "left"]
            case 270:
                return direction in ["down", "left"]
