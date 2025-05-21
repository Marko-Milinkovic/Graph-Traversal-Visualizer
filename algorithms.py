from collections import deque
from settings import *
import heapq
import itertools
import pygame
import math
import random

def reconstruct_path(came_from, end_tile):
    cost = 0
    current = end_tile
    while current in came_from and came_from[current] is not None:  # Stop at start tile
        if not current.is_end:  # Don't recolor the end tile
            current.color = PATH_COLOR  # Use a distinct path color
        cost += current.cost
        current = came_from[current]
        yield
    print("Path cost: {}".format(cost))


def heuristic(a, b):
    # Manhattan distance
    return abs(a.row - b.row) + abs(a.col - b.col)


def bfs_generator(grid):
    start = grid.start_tile
    end = grid.end_tile
    if not start or not end:
        print("Start or end not set!")
        return

    queue = deque()
    came_from = {}  # For reconstructing the path
    visited = set()

    queue.append(start)
    visited.add(start)
    came_from[start] = None

    start_time = pygame.time.get_ticks()

    while queue:
        current = queue.popleft()

        if current == end:
            end_time = pygame.time.get_ticks()
            elapsed_time = (end_time - start_time) / 1000
            print("Time needed to find end tile using BFS*: " + f"{elapsed_time:.2f}s")
            yield from reconstruct_path(came_from, end)
            return

        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                came_from[neighbor] = current
                if not neighbor.is_end:
                    neighbor.color = GREEN  # Mark as explored
                yield


def dfs_generator(grid):
    start = grid.start_tile
    end = grid.end_tile
    if not start or not end:
        print("Start or end not set!")
        return

    stack = [grid.start_tile]
    visited = set()
    came_from = {}

    start_time = pygame.time.get_ticks()

    while stack:
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        # Stop if we reach the end
        if current.is_end:
            break
        current.color = GREEN  # visited
        yield  # pause for step-by-step

        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited and neighbor.walkable:
                stack.append(neighbor)
                came_from[neighbor] = current

    end_time = pygame.time.get_ticks()
    elapsed_time = (end_time - start_time) / 1000
    print("Time needed to find end tile using DFS*: " + f"{elapsed_time:.2f}s")
    yield from reconstruct_path(came_from, current)
    return


def astar_generator(grid):
    start = grid.start_tile
    end = grid.end_tile
    if not start or not end:
        print("Start or end not set!")
        return

    counter = itertools.count()  # Unique sequence count

    open_set = []
    heapq.heappush(open_set, (0, next(counter), start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    visited = set()

    start_time = pygame.time.get_ticks()

    while open_set:
        current_f, _, current = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)

        if current == end:
            end_time = pygame.time.get_ticks()
            elapsed_time = (end_time - start_time) / 1000
            print("Time needed to find end tile using A*: " + f"{elapsed_time:.2f}s")
            yield from reconstruct_path(came_from, current)
            return

        for neighbor in grid.get_neighbors(current):
            tentative_g = g_score[current] + neighbor.cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], next(counter), neighbor))
                if neighbor != end and neighbor != start:
                    neighbor.color = GREEN
        yield


def dfs_limited_iterative(grid, start, goal, depth, visited, came_from):
    stack = [(start, 0)]  # Stack to hold (node, current_depth)
    visited.add(start)

    while stack:
        node, current_depth = stack.pop()

        # If we've reached the goal
        if node == goal:
            return True
        node.color = GREEN
        # If we have not reached the maximum depth
        if current_depth < depth:
            for neighbor in grid.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = node
                    stack.append((neighbor, current_depth + 1))
        yield

    return False


def iddfs_generator(grid):
    start = grid.start_tile
    end = grid.end_tile

    if not start or not end:
        print("Start or end not set!")
        return

    start_time = pygame.time.get_ticks()

    depth = 0
    while True:
        visited = set()
        came_from = {start: None}
        found = False

        dfs_gen = dfs_limited_iterative(grid, start, end, depth, visited, came_from)
        for _ in dfs_gen:
            yield  # Step through the DFS generator

            # Check if goal was visited in this depth
            if end in visited:
                found = True
                break

        if found:
            end_time = pygame.time.get_ticks()
            elapsed_time = (end_time - start_time) / 1000
            print("Time needed to find end tile using A*: " + f"{elapsed_time:.2f}s")
            yield from reconstruct_path(came_from, end)
            return  # Done

        depth += 1


def fringe_generator(grid):
    start = grid.start_tile
    goal = grid.end_tile

    if not start or not goal:
        print("Start or goal not set!")
        return

    came_from = {}
    g_score = {start: 0}
    f_score = heuristic(start, goal)
    threshold = f_score

    now = deque([start])
    later = deque()
    visited = set()
    came_from[start] = None

    start_time = pygame.time.get_ticks()

    while True:
        next_threshold = math.inf

        while now:
            current = now.pop()

            current.color = GREEN
            visited.add(current)

            if current == goal:
                end_time = pygame.time.get_ticks()
                elapsed_time = (end_time - start_time) / 1000
                print("Time needed to find end tile using FRINGE: " + f"{elapsed_time:.2f}s")
                yield from reconstruct_path(came_from, goal)
                return

            for neighbor in grid.get_neighbors(current):
                tentative_g = g_score[current] + neighbor.cost
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    came_from[neighbor] = current
                    f = tentative_g + heuristic(neighbor, goal)

                    if f <= threshold:
                        now.appendleft(neighbor)
                    else:
                        later.appendleft(neighbor)
                        next_threshold = min(next_threshold, f)

            yield  # For visual step-by-step execution

        if not later:
            print("No path found.")
            return

        threshold = next_threshold
        now = later
        later = deque()


def greedybfs_generator(grid):
    start = grid.start_tile
    end = grid.end_tile
    if not start or not end:
        print("Start or end not set!")
        return

    counter = itertools.count()

    open_set = []
    heapq.heappush(open_set, (heuristic(start, end), next(counter), start))

    came_from = {}

    visited = set()

    start_time = pygame.time.get_ticks()

    while open_set:
        current_h, _, current = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)

        if current == end:
            end_time = pygame.time.get_ticks()
            elapsed_time = (end_time - start_time) / 1000
            print("Time needed to find end tile using Greedy Best-First Search: " + f"{elapsed_time:.2f}s")
            yield from reconstruct_path(came_from, current)
            return

        for neighbor in grid.get_neighbors(current):
            if neighbor in visited:
                continue
            came_from[neighbor] = current
            h = heuristic(neighbor, end)
            heapq.heappush(open_set, (h, next(counter), neighbor))
            if neighbor != end and neighbor != start:
                neighbor.color = GREEN
        yield


def bidirectional_bfs_generator(grid):
    start = grid.start_tile
    end = grid.end_tile
    if not start or not end:
        print("Start or end not set!")
        return

    if start == end:
        return

    # Two queues for the two frontiers
    frontier_start = deque([start])
    frontier_end = deque([end])

    # Visited sets and parent maps
    visited_start = {start}
    visited_end = {end}
    parents_start = {start: None}
    parents_end = {end: None}

    start_time = pygame.time.get_ticks()

    while frontier_start and frontier_end:
        # Expand from the start side
        current_start = frontier_start.popleft()
        for neighbor in grid.get_neighbors(current_start):
            if neighbor not in visited_start:
                visited_start.add(neighbor)
                parents_start[neighbor] = current_start
                frontier_start.append(neighbor)
                if neighbor != end and neighbor != start:
                    neighbor.color = GREEN
                if neighbor in visited_end:
                    # Found meeting point
                    meeting_point = neighbor
                    end_time = pygame.time.get_ticks()
                    elapsed = (end_time - start_time) / 1000
                    print(f"Time using Bidirectional BFS: {elapsed:.2f}s")
                    yield from _reconstruct_bidirectional_path(parents_start, parents_end, meeting_point)
                    return
        yield

        # Expand from the goal side
        current_end = frontier_end.popleft()
        for neighbor in grid.get_neighbors(current_end):
            if neighbor not in visited_end:
                visited_end.add(neighbor)
                parents_end[neighbor] = current_end
                frontier_end.append(neighbor)
                if neighbor != start and neighbor != end:
                    neighbor.color = VIBRANT_BLUE
                if neighbor in visited_start:
                    meeting_point = neighbor
                    end_time = pygame.time.get_ticks()
                    elapsed = (end_time - start_time) / 1000
                    print(f"Time using Bidirectional BFS: {elapsed:.2f}s")
                    yield from _reconstruct_bidirectional_path(parents_start, parents_end, meeting_point)
                    return
        yield


def _reconstruct_bidirectional_path(parents_start, parents_end, meeting_point):
    # Reconstruct path from start -> meeting
    path = []
    current = meeting_point
    while current:
        path.append(current)
        current = parents_start[current]
    path.reverse()

    # Reconstruct path from meeting -> end
    current = parents_end[meeting_point]
    while current:
        path.append(current)
        current = parents_end[current]

    for tile in path:
        if tile:
            tile.color = PATH_COLOR
            yield



