import pygame
import math
from src.config import cfg
from src.grid import Cell
from enum import Enum
from random import choice

TILE = cfg.TILE


class Orientation(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


class Robot:
    def __init__(self, cell : Cell) -> None:
        self.occupied_cell = cell
        self.center_x =  cell.x + (TILE // 2)
        self.center_y = cell.y + (TILE // 2)
        self.target_x = self.center_x
        self.target_y = self.center_y
        self.facing = Orientation.UP
        self.radius = (TILE // 3)
        self.rotating_left = False
        self.rotating_right = False
        self.moving_forward = False
        self.hitting_wall = False
        self.reverse = False
        self.line_end_x = self.center_x
        self.line_end_y = self.center_y - (TILE // 2)
        self.theta = 270
        self.target_theta = 270
        self.line_radius = TILE // 2
        self.line_thickness = 4

    def draw_robot(self, screen) -> None:

        if self.hitting_wall:
            if self.facing == Orientation.UP:
                self.center_y -= 1
            elif self.facing == Orientation.DOWN:
                self.center_y += 1
            elif self.facing == Orientation.RIGHT:
                self.center_x += 1
            elif self.facing == Orientation.LEFT:
                self.center_x -= 1
            if self.center_x == self.target_x and self.center_y == self.target_y:
                self.hitting_wall = False
                self.reverse = True
                self.target_x = self.occupied_cell.x + (TILE // 2)
                self.target_y = self.occupied_cell.y + (TILE // 2)

        if self.reverse:
            if self.facing == Orientation.UP:
                self.center_y += 1
            elif self.facing == Orientation.DOWN:
                self.center_y -= 1
            elif self.facing == Orientation.RIGHT:
                self.center_x -= 1
            elif self.facing == Orientation.LEFT:
                self.center_x += 1
            if self.center_x == self.target_x and self.center_y == self.target_y:
                self.reverse = False
        # draw the circle robot
        pygame.draw.circle(screen, pygame.Color("#ff2626"), (self.center_x,self.center_y), self.radius)
        
        # draw the orientation line
        if self.rotating_right:
            self.theta += 1
            self.line_end_x = (self.line_radius * math.cos(math.radians(self.theta))) + self.center_x
            self.line_end_y = (self.line_radius * math.sin(math.radians(self.theta))) + self.center_y 
            if self.theta == self.target_theta:
                self.rotating_right = False
        elif self.rotating_left:
            self.theta -= 1
            self.line_end_x = (self.line_radius * math.cos(math.radians(self.theta))) + self.center_x
            self.line_end_y = (self.line_radius * math.sin(math.radians(self.theta))) + self.center_y 
            if self.theta == self.target_theta:
                self.rotating_left = False
        
        pygame.draw.line(screen, pygame.Color('#0ad100'),
                    (self.center_x, self.center_y),
                    (self.line_end_x, self.line_end_y), self.line_thickness)



    
    def move_forward(self) -> None:
        if self.can_move_forward():
            self.moving_forward = True
        else:
            self.hitting_wall = True
            if self.facing == Orientation.UP:
                self.target_y -= 9
            elif self.facing == Orientation.DOWN:
                self.target_y += 9
            elif self.facing == Orientation.RIGHT:
                self.target_x += 9
            elif self.facing == Orientation.LEFT:
                self.target_x -= 9
    
    def can_move_forward(self) -> bool:
        return False
        if self.facing == Orientation.UP and not self.occupied_cell.walls['top']:
            return True
        elif self.facing == Orientation.DOWN and not self.occupied_cell.walls['bottom']:
            return True
        elif self.facing == Orientation.LEFT and not self.occupied_cell.walls['left']:
            return True
        elif self.facing == Orientation.RIGHT and not self.occupied_cell.walls['right']:
            return True
        else:
            return False

    def rotate_left(self) -> None:
        if self.facing == Orientation.UP:
            self.facing = Orientation.LEFT
        elif self.facing == Orientation.DOWN:
            self.facing == Orientation.RIGHT
        elif self.facing == Orientation.LEFT:
            self.facing == Orientation.DOWN
        elif self.facing == Orientation.RIGHT:
            self.facing == Orientation.UP
        self.rotating_left = True
        self.target_theta -= 90

    def rotate_right(self) -> None:
        if self.facing == Orientation.UP:
            self.facing = Orientation.RIGHT
        elif self.facing == Orientation.DOWN:
            self.facing = Orientation.LEFT
        elif self.facing == Orientation.LEFT:
            self.facing = Orientation.UP
        elif self.facing == Orientation.RIGHT:
            self.facing = Orientation.DOWN
        self.rotating_right = True
        self.target_theta += 90

    def toggle_rotation(self) -> None:
        c = choice([0,1])
        if c:
            self.rotate_left()
        else:
            self.rotate_right()

