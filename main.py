import pygame
from settings import *
from grid import Grid
from visualizer import Visualizer
from button import Button
from algorithms import *
from mazeJSON import *
from labyrinth import *

pygame.init()

algorithm_generator = None
algorithm_mode = "BFS"
current_mode = "block"

font = pygame.font.SysFont("Arial", 28)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Algorithm Visualizer")
clock = pygame.time.Clock()

grid = Grid()
visualizer = Visualizer(grid)

last_step_time = pygame.time.get_ticks()  # Initialize last_step_time


def set_mode_start():
    global current_mode
    current_mode = "start"
    on_algorithm_button_clicked(button_start)


def set_mode_end():
    global current_mode
    current_mode = "end"
    on_algorithm_button_clicked(button_end)


def set_mode_block():
    global current_mode
    current_mode = "block"
    on_algorithm_button_clicked(button_block)


def on_algorithm_button_clicked(selected_button):
    if selected_button.text not in ["BFS", "DFS", "A*", "IDDFS", "FRINGE", "GREEDY BFS", "BIDIRECT BFS"]:
        return
    for button in [button_bfs, button_dfs, button_astar, button_iddfs, button_fringe, button_greedy, button_bidirectional]:
        button.is_active = False  # Deactivate other algorithm buttons
    selected_button.is_active = True  # Set the selected button to active


# Define your algorithm button functions
def set_bfs():
    global algorithm_mode
    algorithm_mode = "BFS"
    on_algorithm_button_clicked(button_bfs)


def set_dfs():
    global algorithm_mode
    algorithm_mode = "DFS"
    on_algorithm_button_clicked(button_dfs)


def set_astar():
    global algorithm_mode
    algorithm_mode = "A*"
    on_algorithm_button_clicked(button_astar)


def set_iddfs():
    global algorithm_mode
    algorithm_mode = "IDDFS"
    on_algorithm_button_clicked(button_iddfs)


def set_fringe():
    global algorithm_mode
    algorithm_mode = "FRINGE"
    on_algorithm_button_clicked(button_fringe)


def set_greedy():
    global algorithm_mode
    algorithm_mode = "GREEDY"
    on_algorithm_button_clicked(button_greedy)


def set_bidirectional():
    global algorithm_mode
    algorithm_mode = "BIDIRECTIONAL"
    on_algorithm_button_clicked(button_bidirectional)


def run_algorithm():
    global algorithm_generator
    grid.clear_path()

    if algorithm_mode == "BFS":
        algorithm_generator = bfs_generator(grid)
    elif algorithm_mode == "DFS":
        algorithm_generator = dfs_generator(grid)
    elif algorithm_mode == "A*":
        algorithm_generator = astar_generator(grid)
    elif algorithm_mode == "IDDFS":
        algorithm_generator = iddfs_generator(grid)
    elif algorithm_mode == "FRINGE":
        algorithm_generator = fringe_generator(grid)
    elif algorithm_mode == "GREEDY":
        algorithm_generator = greedybfs_generator(grid)
    elif algorithm_mode == "BIDIRECTIONAL":
        algorithm_generator = bidirectional_bfs_generator(grid)
    elif algorithm_mode == "STOP":
        algorithm_generator = None
    else:
        return


def on_algorithm_selected(name):
    global algorithm_mode
    algorithm_mode = name
    print("Selected algorithm:", algorithm_mode)


def clear_grid():
    global grid
    grid.clear()
    global algorithm_mode
    algorithm_mode = "STOP"
    run_algorithm()

def get_description():
    print("Hello world")

button_width = 140
button_height = 30
spacing = 20
y_pos = SCREEN_HEIGHT - 200

# Total width of all elements (4 buttons + 1 dropdown + spacing)
total_width = 5 * button_width + 4 * spacing
start_x = (SCREEN_WIDTH - total_width) // 2  # Center everything

# Default buttons
button_start = Button("Set Start", start_x, y_pos + 20, button_width, button_height, set_mode_start)
button_end = Button("Set Goal", start_x + (button_width + spacing) * 1, y_pos + 20, button_width, button_height, set_mode_end)
button_block = Button("Block Mode", start_x + (button_width + spacing) * 2, y_pos + 20, button_width, button_height, set_mode_block)
button_run = Button("Run (Enter)", start_x + (button_width + spacing) * 3, y_pos + 4 * button_height - 20, button_width, button_height, run_algorithm)
button_save = Button("Save Grid", start_x + (button_width + spacing) * 4, y_pos + 20, button_width, button_height, lambda: export_maze_to_json(grid))
button_load = Button("Load Grid", start_x + (button_width + spacing) * 4, y_pos + 2 * button_height, button_width, button_height, lambda: load_maze_from_json(grid))
button_clear = Button("Clear Grid", start_x + (button_width + spacing) * 4, y_pos + 4 * button_height - 20, button_width, button_height, clear_grid)

button_bfs = Button("BFS", start_x, y_pos + 2 * button_height, button_width, button_height, set_bfs)
button_dfs = Button("DFS", start_x + (button_width + spacing) * 1, y_pos + 2 * button_height, button_width, button_height, set_dfs)
button_astar = Button("A*", start_x + (button_width + spacing) * 2, y_pos + 2 * button_height, button_width, button_height, set_astar)
button_iddfs = Button("IDDFS", start_x + (button_width + spacing) * 3, y_pos + 2 * button_height, button_width, button_height, set_iddfs)
button_fringe = Button("FRINGE", start_x, y_pos + 4 * button_height - 20, button_width, button_height, set_fringe)
button_greedy = Button("GREEDY BFS", start_x + (button_width + spacing) * 1, y_pos + 4 * button_height - 20, button_width, button_height, set_greedy)
button_bidirectional = Button("BIDIRECT BFS", start_x + (button_width + spacing) * 2, y_pos + 4 * button_height - 20, button_width, button_height, set_bidirectional)

button_labyrinth = Button("LABYRINTH", start_x + (button_width + spacing) * 3, y_pos + 20, button_width, button_height, lambda: generate_maze(grid))


button_decription = Button("Visualizer Description", start_x, y_pos + 5 * button_height - 10, button_width * 5 + 80, button_height, get_description)

buttons = [button_start, button_end, button_block, button_run, button_bfs, button_dfs, button_astar, button_iddfs, button_fringe,
           button_save, button_load, button_clear, button_decription, button_greedy, button_bidirectional, button_labyrinth]

# Dropdown next to the last button
#dropdown_algo = Dropdown(start_x + (button_width + spacing) * 4, y_pos + 20, button_width, button_height,
                         #["BFS", "DFS", "A*", "IDDFS", "FRINGE"],
                         #on_algorithm_selected)


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():

        for button in buttons:
            button.handle_event(event)

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                grid.set_cost_tile(mouse_pos)  # Set costly tile with Ctrl+Click
            elif mouse_pos[1] < GRID_ROWS * TILE_SIZE:
                if current_mode == "start":
                    grid.set_start(mouse_pos)
                elif current_mode == "end":
                    grid.set_end(mouse_pos)
                elif current_mode == "block":
                    grid.toggle_block(mouse_pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                run_algorithm()
            if event.key == pygame.K_e:  # Press 'e' to export the maze to JSON
                export_maze_to_json(grid)
            elif event.key == pygame.K_l:  # Press 'l' to load the maze from JSON
                load_maze_from_json(grid)

        # Handle dropdown events
        #dropdown_algo.handle_event(event)

    # Draw everything
    screen.fill(CHARCOAL)
    visualizer.draw(screen)

    for button in buttons:
        button.draw(screen)


    #dropdown_algo.draw(screen)

    # Algorithm step-by-step execution
    if algorithm_generator:
        now = pygame.time.get_ticks()
        if now - last_step_time >= STEP_DELAY:
            try:
                next(algorithm_generator)  # Advance one step
                last_step_time = now

            except StopIteration:
                algorithm_generator = None  # Done
                timer_running = False


    pygame.display.flip()

pygame.quit()
