import pygame
from settings import *


class Tile:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.walkable = True
        self.color = GRID_FILL
        self.is_start = False
        self.is_end = False
        self.is_path = False  # For visualization after algorithm runs
        self.cost = 1  # Default cost is 1

    def draw(self, surface):
        # Fill background color
        if not self.walkable:
            pygame.draw.rect(surface, (40, 40, 40), self.rect)
        elif self.is_start:
            pygame.draw.rect(surface, START_TILE, self.rect)
        elif self.is_end:
            pygame.draw.rect(surface, GOAL_TILE, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, GRID_BORDER, self.rect, 1)

    def set_blocked(self):
        self.walkable = False
        self.color = (40, 40, 40)

    def set_clear(self):
        self.walkable = True
        self.color = GRID_FILL
        self.is_start = False
        self.is_end = False
        self.cost = 1

    def set_start(self):
        self.is_start = True
        self.walkable = True
        self.color = START_TILE

    def set_end(self):
        self.is_end = True
        self.walkable = True
        self.color = GOAL_TILE

    def set_costly(self, cost=5):
        self.cost = cost
        self.color = ORANGE

    def reset(self):
        self.is_blocked = False
        self.is_start = False
        self.is_end = False
        self.is_cost = False
        self.g = float('inf')
        self.h = float('inf')
        self.f = float('inf')
        self.color = GRAY
        self.walkable = True
        self.cost = 1

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return isinstance(other, Tile) and self.row == other.row and self.col == other.col


class Grid:

    def __init__(self):
        self.rows = GRID_ROWS
        self.cols = GRID_COLS
        self.tiles = [[Tile(row, col) for col in range(self.cols)] for row in range(self.rows)]
        self.changed = False  # NEW
        self.start_tile = None
        self.end_tile = None

    def draw(self, surface):
        for row in self.tiles:
            for tile in row:
                tile.draw(surface)

    def get_tile_at_pos(self, pos):
        x, y = pos
        col = x // TILE_SIZE
        row = y // TILE_SIZE
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.tiles[row][col]
        return None

    def toggle_block(self, pos):
        tile = self.get_tile_at_pos(pos)
        if tile and not tile.is_start and not tile.is_end:
            if tile.walkable:
                tile.set_blocked()
            else:
                tile.set_clear()
            self.changed = True  # Flag the grid as changed

    def set_start(self, pos):
        tile = self.get_tile_at_pos(pos)
        if tile and tile.walkable and not tile.is_end:
            # Clear previous start
            if self.start_tile:
                self.start_tile.is_start = False
                self.start_tile.color = GRID_FILL
            tile.is_start = True
            tile.color = START_TILE
            self.start_tile = tile
            self.changed = True

    def set_end(self, pos):
        tile = self.get_tile_at_pos(pos)
        if tile and tile.walkable and not tile.is_start:
            if self.end_tile:
                self.end_tile.is_end = False
                self.end_tile.color = GRID_FILL
            tile.is_end = True
            tile.color = GOAL_TILE
            self.end_tile = tile
            self.changed = True

    def set_cost_tile(self, pos):
        tile = self.get_tile_at_pos(pos)
        if tile and tile.walkable and not tile.is_start and not tile.is_end:
            tile.set_costly()
            self.changed = True

    def get_neighbors(self, tile):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for drow, dcol in directions:
            row = tile.row + drow
            col = tile.col + dcol
            if 0 <= row < self.rows and 0 <= col < self.cols:
                neighbor = self.tiles[row][col]
                if neighbor.walkable:
                    neighbors.append(neighbor)
        return neighbors

    def clear_path(self):
        for row in self.tiles:
            for tile in row:
                if not tile.is_start and not tile.is_end and tile.walkable and tile.cost != 5:
                    tile.color = GRID_FILL

    def clear(self):
        for row in self.tiles:
            for tile in row:
                tile.reset()  # Reset each tile (unblock, remove cost, etc.)

        self.start = None  # Clear the start tile
        self.end = None  # Clear the end tile
        self.cost_tiles = []  # Clear the cost tiles

    def reset_changed_flag(self):
        self.changed = False


