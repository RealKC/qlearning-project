import random
from visuals import TileMap, Tile, Coordinate, directions, Direction


class QLEnvironment:
    """
    A class representing the 2D environment that our agent exists within.

    Actions are mapped as follows:
    * 0: Up
    * 1: Right
    * 2: Down
    * 3: Left

    Observations about the environment are mapped by the formula $x \\cdot width + y$
    """

    tilemap: TileMap

    initial_coordinate: Coordinate

    current_state: float

    def __init__(self, tilemap: TileMap, initial_coordinate: Coordinate):
        self.tilemap = tilemap
        self.initial_coordinate = initial_coordinate

        self.transition_matrix = {
            s: {a: () for a in range(self.n_actions)}
            for s in range(self.n_observations)
        }

        def move(action: Direction, x: int, y: int) -> float:
            match action:
                case "left":
                    return self._position_to_state(max(0, x - 1), y)
                case "right":
                    return self._position_to_state(min(x + 1, tilemap.width - 1), y)
                case "up":
                    return self._position_to_state(x, max(0, y - 1))
                case "down":
                    return self._position_to_state(x, max(y + 1, tilemap.height - 1))

        for s in range(self.n_observations):
            x = s // tilemap.width
            y = s % tilemap.width

            print(f"# state={s} -> {x}x{y}")

            tile: Tile = tilemap.tiles[x][y]

            mask = [0, 0, 0, 0]
            for i, dir in enumerate(directions):
                if tile.can_go_to(dir):
                    mask[i] = 1

            n = sum(mask)
            if n == 0:
                n = 1

            probabilities = list(map(lambda x: x / n, mask))

            for a in range(self.n_actions):
                terminated = tilemap.is_goal(tile.coord)
                reward = 1 if terminated else 0

                self.transition_matrix[s][a] = (
                    move(directions[a], x, y),
                    reward,
                    terminated,
                    probabilities[a],
                )

    def reset(self) -> float:
        self.tilemap.move_agent(self.initial_coordinate)
        self.current_state = self._position_to_state(
            self.tilemap.agent[0], self.tilemap.agent[1]
        )

        return self.current_state

    def _position_to_state(self, x: float, y: float) -> float:
        return x * self.tilemap.width + y

    @property
    def n_actions(self) -> float:
        return 4

    @property
    def n_observations(self) -> float:
        return self.tilemap.width * self.tilemap.height

    def sample_action(self) -> float:
        transitions = self.transition_matrix[self.current_state]

        choices = []

        for i, t in enumerate(transitions.values()):
            if t[3] > 0:
                choices.append(i)

        chosen = random.choice(choices)

        return chosen

    def step(self, action) -> tuple[float, float, bool]:
        next, reward, terminated, p = self.transition_matrix[self.current_state][action]
        self.current_state = next

        return next, reward, terminated
