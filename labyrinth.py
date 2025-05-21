import random

def generate_maze(grid):
    grid.clear()
    grid.reset_changed_flag()

    stack = []

    # Fill all tiles with walls first
    for row in grid.tiles:
        for tile in row:
            tile.set_blocked()

    # Pick a random starting point (odd row and col)
    start_row = random.randrange(1, grid.rows, 2)
    start_col = random.randrange(1, grid.cols, 2)
    start_tile = grid.tiles[start_row][start_col]
    start_tile.set_clear()

    stack.append(start_tile)

    while stack:
        current = stack[-1]
        row, col = current.row, current.col

        # Check for unvisited neighbors 2 steps away
        neighbors = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for drow, dcol in directions:
            nrow, ncol = row + drow, col + dcol
            if 0 <= nrow < grid.rows and 0 <= ncol < grid.cols:
                neighbor = grid.tiles[nrow][ncol]
                if not neighbor.walkable:  # Still a wall => unvisited
                    neighbors.append((neighbor, drow, dcol))

        if neighbors:
            neighbor, drow, dcol = random.choice(neighbors)
            # Carve path between current and neighbor
            wall_row = row + drow // 2
            wall_col = col + dcol // 2
            grid.tiles[wall_row][wall_col].set_clear()
            neighbor.set_clear()
            stack.append(neighbor)
        else:
            stack.pop()

    grid.changed = True

