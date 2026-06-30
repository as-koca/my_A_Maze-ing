import sys
from maze_data import Maze
from parser import Config
from output import write_maze
from collections.abc import Callable
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


def draw_maze(stdscr: curses.window,
              maze: Maze,
              entry: tuple[int, int],
              exit: tuple[int, int],
              pattern: set[tuple[int, int]],
              path_coords: set[tuple[int, int]],
              show_path: bool = False,
              palette: int = 0) -> None:
    """
        Draws every wall and cell of the maze with position-centric rendering.

        - Checks if on a corner, horizontal or vertical wall, or a cell.
        - Checks presence of wall by mapping position to maze coordinate then
        looks in each direction for wall.
        - Rendering done using empty blocks (space char) which are colored to
        show a wall or passage.
        - Screens `col` coordinate multiplied by 2 since we print 2 spaces,
        and curses automatically prints onto col0 --> coln for 'n' characters.
        """

    wall_pair: int = 1 if palette == 0 else 3
    path_pair: int = 2 if palette == 0 else 4
    passage_pair: int = 8

    for row in range(2 * maze.height + 1):
        for col in range(2 * maze.width + 1):
            mx = col // 2
            my = (maze.height - 1) - (row // 2)
            if is_even(row) and is_even(col):
                stdscr.addstr(row, col * 2, "  ", curses.color_pair(wall_pair))
            elif is_even(row):
                above_y = my + 1
                if 0 <= my < maze.height:
                    closed = maze.has_wall(mx, my, "N")
                else:
                    closed = maze.has_wall(mx, above_y, "S")
                pair: int = wall_pair if closed else passage_pair
                stdscr.addstr(row, col * 2, "  ", curses.color_pair(pair))
            elif is_even(col):
                left_x = mx - 1
                if 0 <= mx < maze.width:
                    closed = maze.has_wall(mx, my, "W")
                else:
                    closed = maze.has_wall(left_x, my, "E")
                pair = wall_pair if closed else passage_pair
                stdscr.addstr(row, col * 2, "  ", curses.color_pair(pair))
            else:
                if (mx, my) == entry:
                    pair = 5
                elif (mx, my) == exit:
                    pair = 6
                elif (mx, my) in pattern:
                    pair = 7
                elif show_path and (mx, my) in path_coords:
                    pair = path_pair
                else:
                    pair = passage_pair
                stdscr.addstr(row, col * 2, "  ", curses.color_pair(pair))


def render_maze(stdscr: curses.window,
                maze: Maze, config: Config,
                pattern: set[tuple[int, int]],
                path_coords: set[tuple[int, int]],
                generate_maze: Callable) -> None:
    curses.start_color()
    # palette 1 (walls + path)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)    # wall
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)     # path
    # palette 2 (walls + path)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)   # wall
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)     # path
    # fixed colors
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)    # entry
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_RED)      # exit
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_MAGENTA)  # 42 pattern
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)    # passage

    curses.curs_set(0)

    palette: int = 0
    show_path: bool = False
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        needed_y = 2 * maze.height + 1
        needed_x = (2 * maze.width + 1) * 2
        if needed_y > max_y or needed_x > max_x:
            stdscr.clear()
            msg = "Terminal too small. Resize."
            stdscr.addstr(0, 0, msg)
            stdscr.refresh()
            stdscr.getch()
        else:
            draw_maze(stdscr, maze,
                      config.entry, config.exit,
                      pattern, path_coords,
                      show_path, palette)
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord("q"):
                break
            elif key == ord("c"):
                palette = 1 - palette
            elif key == ord("p"):
                show_path = not show_path
            elif key == ord("r"):
                maze, solved_path, pattern, path_coords = generate_maze(
                    config)
                write_maze(maze, config.entry, config.exit,
                           solved_path, config.output_file)


# KEY_RESIZE when resizing the window gets passed to getch()

if __name__ == "__main__":
    maze = Maze(20, 15)
    patt = maze.make_pattern_anchors()
    maze.carve_maze((0, 0), seed=100, blocked=patt)
    path = maze.solve((0, 0), (19, 14))
    path_coords = maze.get_path_coords(path, (0, 0))

    curses.wrapper(lambda stdscr: draw_maze(
        stdscr, maze, (0, 0), (19, 14), patt, path_coords))


# print("|" if closed else " ", end='')
# print("+", end='')
# print("---" if closed else "   ", end="")
# print("|" if closed else " ", end="")
# print("ENT", end='')
# print("EXI", end='')
# print("###", end='')
# print(" o ", end='')
# print("   ")

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
