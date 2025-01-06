import numpy as np

from qlenv import QLEnvironment


class QLearningAgent:
    n_observations: int
    n_actions: int

    exploration_probability: float
    learning_rate: float
    gamma: float
    decay_constant: float

    environment: QLEnvironment

    table: np.ndarray

    rewards: list[float]

    _current_visual_state: float

    def __init__(self, n_observations: int, n_actions: int, environment: QLEnvironment):
        self.n_actions = n_actions
        self.n_observations = n_observations
        self.environment = environment

        self.exploration_probability = 1.0
        self.learning_rate = 0.1
        self.gamma = 0.75
        self.decay_constant = 0.001

        self.table = np.zeros((n_observations, n_actions))

        self.rewards = []

        self._current_visual_state = 0

    def train(self, episode_count: int, max_iterations=100):
        self.rewards = []

        for _ in range(0, episode_count):
            self.rewards.append(self._do_episode_iteration(max_iterations))

    def _do_episode_iteration(self, max_iterations: int) -> float:
        current_state = self.environment.reset()

        total_reward = 0.0

        for i in range(max_iterations):
            current_state = self._do_episode_iteration_step(current_state)

            if current_state is None:
                break

        self.exploration_probability = max(0.1, np.exp(-self.decay_constant * i))

        return total_reward

    def visual_reset(self):
        self._current_visual_state = self.environment.reset()
        self.exploration_probability = 0

    def do_visual_step(self) -> bool:
        cs = self._do_episode_iteration_step(self._current_visual_state, visual=True)

        if cs is None:
            return True

        self._current_visual_state = cs
        return False

    def _do_episode_iteration_step(
        self, current_state: float, visual: bool = False
    ) -> float | None:
        if np.random.uniform(0, 1) < self.exploration_probability:
            action = self.environment.sample_action()
        else:
            action = np.argmax(self.table[current_state, :])

        next_state, reward, done = self.environment.step(action, visual)
        # fmt: off
        self.table[current_state, action] = (1 - self.learning_rate) * self.table[current_state, action] + self.learning_rate * (reward + self.gamma * max(self.table[next_state, :]))
        # fmt: on

        if done:
            return None

        return next_state
