import os
import pygame
from ql import QLearningAgent
from qlenv import QLEnvironment
from visuals import render_map
import matplotlib.pyplot as plt


# pygame setup
pygame.init()
pygame.font.init()

tilemap = render_map("03240\n01010\n06250", (2, 3), (0, 1))

environment = QLEnvironment(tilemap, (0, 1))

agent = QLearningAgent(environment.n_observations, environment.n_actions, environment)
agent.train(episode_count=10_000)

print(agent.table)

if os.getenv("EXPORT_FIGURE") == "1":
    fig, ax = plt.subplots()
    ax.set_title("Rewards")
    ax.plot(range(0, len(agent.rewards)), agent.rewards)
    fig.savefig("fig.png")

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    tilemap.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
