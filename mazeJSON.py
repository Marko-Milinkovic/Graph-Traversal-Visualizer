import json
from settings import *


def export_maze_to_json(grid, filename="maze.json"):
    maze_data = {
        "start": {"row": grid.start_tile.row, "col": grid.start_tile.col} if grid.start_tile else None,
        "end": {"row": grid.end_tile.row, "col": grid.end_tile.col} if grid.end_tile else None,
        "tiles": []
    }

    # Add grid tiles' walkability and costs to the JSON structure
    for row in grid.tiles:
        row_data = []
        for tile in row:
            tile_data = {
                "walkable": tile.walkable,
                "cost": tile.cost if hasattr(tile, 'cost') else 1,  # Default cost is 1 if no specific cost
                "color": tile.color
            }
            row_data.append(tile_data)
        maze_data["tiles"].append(row_data)

    # Save the data to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(maze_data, json_file, indent=4)
    print(f"Maze exported to {filename}")


def load_maze_from_json(grid, filename="maze.json"):

    with open(filename, 'r') as json_file:
        maze_data = json.load(json_file)
    print(f"Maze loaded from {filename}")
    # Clear current grid
    for row in grid.tiles:
        for tile in row:
            tile.set_clear()

    # Load start and end positions
    if maze_data["start"]:
        start_pos = maze_data["start"]
        grid.set_start((start_pos["col"] * TILE_SIZE, start_pos["row"] * TILE_SIZE))

    if maze_data["end"]:
        end_pos = maze_data["end"]
        grid.set_end((end_pos["col"] * TILE_SIZE, end_pos["row"] * TILE_SIZE))

    # Load tile costs and walkability
    for row_idx, row_data in enumerate(maze_data["tiles"]):
        for col_idx, tile_data in enumerate(row_data):
            tile = grid.tiles[row_idx][col_idx]
            tile.walkable = tile_data["walkable"]
            tile.color = tile_data["color"]
            if tile_data["cost"] > 1:
                tile.set_costly(tile_data["cost"])  # Set costly tiles

