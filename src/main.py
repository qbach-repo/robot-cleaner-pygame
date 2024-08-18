# Example file showing a basic pygame "game loop"
import pygame
from src.grid import Grid, Cell
from src.robot import Robot, PolicyRobot
from src.config import cfg


RES = cfg.RES
# pygame setup


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        pygame.display.set_caption('Robot Cleaner')
        self.clock = pygame.time.Clock()
        self.grid = Grid()
        self.robot = Robot(cell=self.grid.grid_cells[0])
        self.running = True
    
    def run_main_loop(self) -> None:
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill(pygame.Color('#a6d5e2'))

            # RENDER YOUR GAME HERE
            self.grid.draw_grid(screen=self.screen)
            if not self.grid.grid_initialized:
                self.grid.initialize_grid(screen=self.screen)
            elif not self.grid.grid_explore_cleanable:
                self.grid.bfs()
                self.grid.grid_explore_cleanable = True
                self.robot.policy_robot = PolicyRobot(grid_cells=self.grid.grid_cells)
                self.robot.policy_robot.dfs_policy()
                self.robot.dfs_policies = self.robot.policy_robot.policies
                # print(self.robot.dfs_policies)
            else:
                self.robot.draw_robot(screen=self.screen)
                # if not self.robot.rotating_left and not self.robot.rotating_right:
                #     self.robot.toggle_rotation()
                if not self.robot.is_busy:
                    self.robot.move()
                    #print(f"action: {self.robot.current_action}, x: {self.robot.center_x}, y: {self.robot.center_y}, orientation: {self.robot.facing}")


            pygame.display.flip()

            self.clock.tick(3000)  # limits FPS to 60


if __name__ == "__main__":
    game = Game()
    game.run_main_loop()