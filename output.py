from maze_data import Maze


def write_maze(
    maze: Maze,
    entry: tuple[int, int],
    exit: tuple[int, int],
    path: list[str],
    output_file: str
) -> None:
    with open(output_file, "w") as fd:
        for row in reversed(maze.storage):
            fd.write("".join(f"{cell:X}" for cell in row) + "\n")
        fd.write("\n")
        fd.write(f"{entry[0]},{entry[1]}\n")
        fd.write(f"{exit[0]},{exit[1]}\n")
        fd.write("".join(path) + "\n")

        # --- ADDED THIS THIS LINE (ALI) --- #
        print(f"Output written into {output_file}")
