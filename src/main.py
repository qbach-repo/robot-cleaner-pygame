# Example file showing a basic pygame "game loop"
import pygame
from src.grid import Grid, Cell
from src.robot import Robot
from src.config import cfg


RES = cfg.RES
# pygame setup


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.grid = Grid()
        self.robot = Robot(cell=self.grid.grid_cells[0])
        self.runing = True
    
    def run_main_loop(self) -> None:
        while self.runing:
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
            else:
                self.robot.draw_robot(screen=self.screen)
                # if not self.robot.rotating_left and not self.robot.rotating_right:
                #     self.robot.toggle_rotation()
                if not self.robot.hitting_wall and not self.robot.reverse:
                    self.robot.move_forward()

            pygame.display.flip()

            self.clock.tick(30)  # limits FPS to 60


if __name__ == "__main__":
    game = Game()
    game.run_main_loop()