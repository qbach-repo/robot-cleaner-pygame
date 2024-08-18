import pygame
from src.grid import Grid, Cell
from src.config import cfg
from src.robot import PolicyRobot

RES = cfg.RES


pygame.init()
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
grid = Grid()
running = True
got_policies = False
policies = []
printed_policies = False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(pygame.Color('#a6d5e2'))

    # RENDER YOUR GAME HERE
    grid.draw_grid(screen=screen)
    if not grid.grid_initialized:
        grid.initialize_grid(screen=screen)
    elif not got_policies:
        policy_robot = PolicyRobot(grid_cells=grid.grid_cells)
        policy_robot.dfs_policy()
        policies = policy_robot.policies
        got_policies = True
    elif not printed_policies:
        print(policies)
        printed_policies = True


    pygame.display.flip()

    clock.tick(120)  # limits FPS to 60