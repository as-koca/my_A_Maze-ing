import sys
import curses
from time import time
from parser import read_config, verify_file, Config
from maze_data import Maze
from output import write_maze
from render import render_maze

# Decided width of maze should be at least 10 for the 42 pattern to be included
# Decided height should be at least 9 -> to have at least 2 cells around pattrn
"""Can get a curses error if terminal window is smaller than maze bounds!"""


def generate_maze(config: Config | None,
                  seed: int | None = None) -> tuple[Maze,
                                                    list[str],
                                                    set[tuple[int, int]],
                                                    set[tuple[int, int]]]:
    """Game logic, carves and solves maze with given configuration and
        writes output to a designated file.

        Returns: Maze, Solved Path, Pattern, Path Coords. In that order."""

    """Preliminary validation checks before game logic"""
    if not config:
        sys.exit()
    pattern_fits: bool = True
    pattern_cells: set[tuple[int, int]] = set()
    maze = Maze(config.width, config.height)
    if seed is not None:
        active_seed: int = seed
    elif config.seed is not None:
        active_seed = config.seed
    else:
        active_seed = int(time())
    if config.width < 10:
        print("Can not include '42' pattern into maze because of", end=' ')
        print("width (min: 10), Proceeding without it...")
        pattern_fits = False
    if config.height < 9:
        print("Can not include '42' pattern into maze because of", end=' ')
        print("height (min: 9), Proceeding without it...")
        pattern_fits = False
    if pattern_fits:
        pattern_cells = maze.make_pattern_anchors()

    """Game logic for perfect and unperfect maze,
        seperated into an if else block"""
    solved_path: list[str] | None = None
    carve_attempts: int = 0
    while solved_path is None and carve_attempts < 100:
        maze = Maze(config.width, config.height)
        if config.perfect:
            maze.carve_maze(config.entry, active_seed +
                            carve_attempts, pattern_cells)
        else:
            maze.carve_unperfect_maze(config.entry, active_seed +
                                      carve_attempts, pattern_cells)
        solved_path = maze.solve(config.entry, config.exit)
        carve_attempts += 1
        if carve_attempts == 2:
            print("Carving failed, attempting with new seeds...")

    if carve_attempts == 100:
        print("Failed to find an exit path with '42' pattern", end=' ')
        print("after 100 attempts, Proceeding without it...")
        maze = Maze(config.width, config.height)
        if config.perfect:
            maze.carve_maze(config.entry, active_seed + 100)
        else:
            maze.carve_unperfect_maze(config.entry, active_seed + 100)
        solved_path = maze.solve(config.entry, config.exit)

    if not solved_path:
        print("No path found to reach exit...")
        sys.exit()
    else:
        path_coords = maze.get_path_coords(solved_path, config.entry)

    print(f"Maze generated with seed: {active_seed + carve_attempts}")
    return (maze, solved_path, pattern_cells, path_coords)


def main() -> None:
    parsed: dict[str, str] = read_config()
    config: Config | None = verify_file(parsed)
    if config is None:
        sys.exit()
    maze, solved_path, pattern, path_coords = generate_maze(config)
    write_maze(maze, config.entry, config.exit,
               solved_path, config.output_file)
    curses.wrapper(lambda stdscr: render_maze(
        stdscr, maze, config, pattern, path_coords, generate_maze))


if __name__ == "__main__":
    main()
