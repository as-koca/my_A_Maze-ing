import sys
from time import time
from my_parser import read_config, verify_file, Config
from maze_data import Maze
from output import write_maze

# Decided width of maze should be at least 10 for the 42 pattern to be included
# Decided height should be at least 9 -> to have at least 2 cells around pattrn


def main() -> None:
    parsed: dict[str, str] = read_config()
    config: Config | None = verify_file(parsed)
    if config is None:
        sys.exit()

    pattern_fits: bool = True
    pattern_cells: set[tuple[int, int]] = set()
    maze = Maze(config.width, config.height)
    if config.seed is None:
        config.seed = int(time())
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

    solved_path: list[str] | None = None
    carve_attempts: int = 0
    while solved_path is None and carve_attempts < 100:
        maze = Maze(config.width, config.height)
        maze.carve_maze(config.entry, config.seed +
                        carve_attempts, pattern_cells)
        solved_path = maze.solve(config.entry, config.exit)
        carve_attempts += 1
    if carve_attempts == 100:
        maze = Maze(config.width, config.height)
        print("Failed to find an exit path with '42' pattern", end=' ')
        print("after 100 attempts, Proceeding without it...")
        maze.carve_maze(config.entry, config.seed + 100)
        solved_path = maze.solve(config.entry, config.exit)
    if not solved_path:
        print("No path found to reach exit...")
        sys.exit()
    else:
        write_maze(maze, config.entry, config.exit,
                   solved_path, config.output_file)


if __name__ == "__main__":
    main()
