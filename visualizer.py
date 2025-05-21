from settings import *


class Visualizer:
    def __init__(self, grid):
        self.grid = grid

    def draw(self, surface):
        self.grid.draw(surface)
