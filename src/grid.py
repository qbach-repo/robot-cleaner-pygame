import pygame
from random import choice
from src.config import cfg

TILE = cfg.TILE
ROWS = cfg.ROWS
COLS = cfg.COLS



class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
    
    def draw_current_cell(self,sc):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('#f70067'),
                         (x + 2, y + 2, TILE - 2, TILE - 2))
    
    def draw(self, sc):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('#1e1e1e'),
                             (x, y, TILE, TILE))
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('#1e4f5b'), 
                             (x, y), (x + TILE, y), 3)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('#1e4f5b'), 
                             (x + TILE, y), 
                             (x + TILE, y + TILE), 3)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('#1e4f5b'), 
                             (x + TILE, y + TILE),
                             (x , y + TILE), 3)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('#1e4f5b'), 
                             (x, y + TILE), (x, y), 3)
            
    def check_cell(self, x, y, grid_cells):
        find_index = lambda x, y: x + y * COLS
        if x < 0 or x > COLS - 1 or y < 0 or y > ROWS - 1:
            return False
        return grid_cells[find_index(x, y)]
    
    def check_neighbors(self,grid_cells):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1,grid_cells)
        right = self.check_cell(self.x + 1, self.y,grid_cells)
        bottom = self.check_cell(self.x, self.y + 1,grid_cells)
        left = self.check_cell(self.x - 1, self.y,grid_cells)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False   
    
    @classmethod
    def remove_walls(cls, current, next):
        dx = current.x - next.x
        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls['top'] = False
            next.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next.walls['top'] = False 

class Grid:

    def __init__(self) -> None:
        self.grid_cells = [Cell(col, row) for row in range(ROWS) for col in range(COLS)]
        self.current_cell = self.grid_cells[0]
        self.stack = []
        self.colors = []
        self.color = 40
        self.grid_initialized = False

    def draw_grid(self,screen) -> None:
        [cell.draw(screen) for cell in self.grid_cells]

    def initialize_grid(self,screen) -> None:
        self.current_cell.visited = True
        self.current_cell.draw_current_cell(screen)
        [pygame.draw.rect(screen, self.colors[i], 
                        (cell.x * TILE + 2, cell.y * TILE + 2,
                        TILE - 4, TILE - 4), border_radius=8) for i,
                        cell in enumerate(self.stack)] 
        
        next_cell = self.current_cell.check_neighbors(grid_cells=self.grid_cells)
        if next_cell:
            next_cell.visited = True
            self.stack.append(self.current_cell)
            self.colors.append((min(self.color, 255), 0, 103))
            self.color += 1
            Cell.remove_walls(self.current_cell, next_cell)
            self.current_cell=next_cell
        elif self.stack: 
            self.current_cell = self.stack.pop()

        if len(self.stack) == 0:
            self.grid_initialized = True