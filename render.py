import sys
from maze_data import Maze
from parser import Config
try:
    import curses
except ModuleNotFoundError as e:
    print(e)
    sys.exit()

# IN CURSES, COLUMS ARE HORIZONTAL (LEFT<->RIGHT)
#            ROWS ARE VERTICAL (UP <-> DOWN)


def is_even(n: int) -> bool:
    if n % 2 == 0:
        return True
    return False


def draw_maze(maze: Maze, entry: tuple[int, int],
              exit: tuple[int, int],
              pattern: set[tuple[int, int]],
              path_coords: set[tuple[int, int]],
              show_path: bool = False) -> None:
    for row in range(2 * maze.height + 1):
        for col in range(2 * maze.width + 1):
            mx = col // 2
            my = (maze.height - 1) - (row // 2)
            if is_even(row) and is_even(col):
                print("+", end='')
            elif is_even(row):
                above_y = my + 1
                if 0 <= my < maze.height:
                    closed = maze.has_wall(mx, my, "N")
                else:
                    closed = maze.has_wall(mx, above_y, "S")
                print("---" if closed else "   ", end="")
            elif is_even(col):
                left_x = mx - 1
                if 0 <= mx < maze.width:
                    closed = maze.has_wall(mx, my, "W")
                else:
                    closed = maze.has_wall(left_x, my, "E")
                print("|" if closed else " ", end='')
            else:
                if (mx, my) == entry:
                    print("ENT", end='')
                elif (mx, my) == exit:
                    print("EXI", end='')
                elif (mx, my) in pattern:
                    print("###", end='')
                elif show_path and (mx, my) in path_coords:
                    print(" o ", end='')
                else:
                    print("   ", end="")
        print("")


maze = Maze(20, 15)
patt = maze.make_pattern_anchors()
maze.carve_maze((0, 0), seed=100, blocked=patt)
path = maze.solve((0, 0), (19, 14))
path_coords = maze.get_path_coords(path, (0, 0))

draw_maze(maze, (0, 0), (19, 14), patt, path_coords, show_path=True)


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


# def draw_maze(maze: Maze, entry: tuple[int, int],
#              exit: tuple[int, int],
#              pattern: set[tuple[int, int]],
#              path_coords: set[tuple[int, int]],
#              show_path: bool = False) -> None:
#    H: int = maze.height
#    W: int = maze.width
#    for y in range(H - 1, -1, -1):
#        for x in range(W):
#            print("+", end='')
#            print("---" if maze.has_wall(x, y, "N") else "   ", end='')
#        print("+")
#        for x in range(W):
#            print("|" if maze.has_wall(x, y, "W") else " ", end='')
#            if (x, y) == entry:
#                print("ENT", end='')
#            elif (x, y) == exit:
#                print("EXI", end='')
#            elif (x, y) in pattern:
#                print("###", end='')
#            elif show_path and (x, y) in path_coords:
#                print(" o ", end='')
#            else:
#                print("   ", end='')
#        print("|")
#    for x in range(W):
#        print("+", end='')
#        print("---" if maze.has_wall(x, 0, "S") else "   ", end='')
#    print("+")
