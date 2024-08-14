from dataclasses import dataclass

@dataclass
class Config:
    RES = WIDTH, HEIGHT = 500, 500
    TILE = 50
    COLS, ROWS = WIDTH // TILE, HEIGHT // TILE

cfg = Config()