from dataclasses import dataclass

@dataclass
class Config:
    RES = WIDTH, HEIGHT = 1200, 900
    TILE = 50
    COLS, ROWS = WIDTH // TILE, HEIGHT // TILE

cfg = Config()