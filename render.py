import sys
from maze_data import Maze
from parser import Config
try:
    import curses
except ModuleNotFoundError as e:
    print(e)
    sys.exit()


def draw_maze(stdscr: curses.window, maze: Maze, entry: tuple[int, int],
              exit: tuple[int, int], pattern: set[tuple[int, int]],
              palette) -> None:


def render_maze(stdscr: curses.window, maze: Maze, config: Config,
                path: list[str], pattern: set[tuple[int, int]]) -> None:
    curses.start_color()
    # palette 1
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # wall
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)  # path
    # palette 2
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # wall
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # path
    # fixed colors
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Entry
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)  # Exit
    curses.init_pair(7, curses.COLOR_MAGENTA,
                     curses.COLOR_BLACK)  # 42 Pattern

    stdscr.addstr(0, 0, "HIIIIIIIIIIIIIIIIIIII" + '\n')
    while True:
        key = stdscr.getch()
        if key == ord("q"):
            break
