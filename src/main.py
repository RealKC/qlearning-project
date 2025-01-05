# Example file showing a basic pygame "game loop"
import pygame
from ql import QLearningAgent
from qlenv import QLEnvironment
from visuals import render_map


# pygame setup
pygame.init()
pygame.font.init()

tilemap = render_map("03240\n01010\n06250", (1, 1), (0, 1))

environment = QLEnvironment(tilemap, (0, 1))

agent = QLearningAgent(environment.n_observations, environment.n_actions, environment)
agent.train(episode_count=10_000)

print(agent.table)
print(agent.rewards)

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    tilemap.draw(screen)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
