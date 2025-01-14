import os
import pygame
from ql import QLearningAgent
from qlenv import QLEnvironment
from visuals import render_map
import matplotlib.pyplot as plt
import numpy as np

# pygame setup
pygame.init()
pygame.font.init()

tilemap = render_map("03224000\n0103+240\n0106+250\n01001000\n06225000", (1, 6), (0, 1))

environment = QLEnvironment(tilemap, (0, 1))

agent = QLearningAgent(environment.n_observations, environment.n_actions, environment)
agent.train(episode_count=10_000)

print(agent.table)

if os.getenv("EXPORT_FIGURE") == "1":
    fig, ax = plt.subplots()
    ax.set_title("Average reward per 1000 episodes")
    mean_rewards = []
    for i in range(10):
        mean_rewards.append(np.mean(agent.rewards[1000 * i : 1000 * (i + 1)]))
    ax.plot(mean_rewards)
    fig.savefig("report/images/results.png")

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

AGENT_VISUAL_STEP = pygame.USEREVENT + 666
pygame.time.set_timer(event=AGENT_VISUAL_STEP, millis=500)

agent.visual_reset()

do_steps = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP and event.key == pygame.K_s:
            do_steps = True

        if event.type == AGENT_VISUAL_STEP and do_steps:
            terminated = agent.do_visual_step()
            if terminated:
                print("terminated")
                pygame.time.set_timer(event=AGENT_VISUAL_STEP, millis=0)

    screen.fill("white")

    tilemap.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
