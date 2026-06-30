import random
from collections import deque

# Direction look-up table:
# "D" : (dx, dy, my_bit, neighbour_bit)
# (dx, dy) -> how to move
bible: dict[str, tuple[int, int, int, int]] = {
    "N": (0, 1, 1, 4),
    "E": (1, 0, 2, 8),
    "S": (0, -1, 4, 1),
    "W": (-1, 0, 8, 2),
}

# '42' pattern flipped upside down, in boolean form.
pattern_42: list[list[bool]] = [
    [False, False, True, False, True, True, True],
    [False, False, True, False, True, False, False],
    [True, True, True, False, True, True, True],
    [True, False, False, False, False, False, True],
    [True, False, False, False, True, True, True]
]
# to center it : we have to anchor to x and y from a direction -> ax, ay
# IF WE HAVE TO RE-CARVE AND THEREFOR CHAND THE SEED --> Print to stdout that
# the SEED was changed!


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.height = height
        self.width = width
        self.storage: list[list[int]] = [
            [15 for _ in range(width)] for _ in range(height)]

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def has_wall(self, x: int, y: int, direction: str) -> bool:
        book = {
            "N": 1,
            "E": 2,
            "S": 4,
            "W": 8,
        }
        bi_direction: int | None = book.get(direction, None)
        if bi_direction is None:
            raise ValueError(
                "ERROR: Unknown Direction, Use: 'N', 'E', 'S' or 'W'")
        cell: int = self.storage[y][x]
        return bool(cell & bi_direction)

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int, str]]:
        potential: list[tuple[int, int, str]] = [
            (x + 1, y, "E"),
            (x - 1, y, "W"),
            (x, y + 1, "N"),
            (x, y - 1, "S")
        ]
        valid: list[tuple[int, int, str]] = [
            (dx, dy, d) for (dx, dy, d) in potential if self.is_valid(dx, dy)
        ]
        return valid

    def remove_wall(self, x: int, y: int, direction: str) -> None:
        valid = self.get_neighbors(x, y)
        if direction not in bible:
            raise ValueError("Error: Invalid Direction")
        neigh_info: tuple[int, int, int, int] = bible[direction]
        dx: int = neigh_info[0]
        dy: int = neigh_info[1]
        b1: int = neigh_info[2]
        b2: int = neigh_info[3]
        if (x + dx, y + dy, direction) not in valid:
            return
        else:
            self.storage[y][x] &= ~b1
            self.storage[y + dy][x + dx] &= ~b2

    def add_wall(self, x: int, y: int, direction: str) -> None:
        valid = self.get_neighbors(x, y)
        if direction not in bible:
            raise ValueError("Error: Invalid Direction")
        neigh_info: tuple[int, int, int, int] = bible[direction]
        dx: int = neigh_info[0]
        dy: int = neigh_info[1]
        b1: int = neigh_info[2]
        b2: int = neigh_info[3]
        if (x + dx, y + dy, direction) not in valid:
            return
        else:
            self.storage[y][x] |= b1
            self.storage[y + dy][x + dx] |= b2

    def carve_maze(
            self, entry: tuple[int, int], seed: int | None = None,
            blocked: set[tuple[int, int]] | None = None) -> None:
        if seed is not None:
            random.seed(seed)
        if blocked is None:
            blocked = set()
        seen: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []
        stack.append(entry)
        seen.add(entry)
        while stack:
            x, y = stack[-1]
            unseen = [i for i in self.get_neighbors(
                x, y) if (i[0], i[1]) not in seen and
                (i[0], i[1]) not in blocked]
            if not unseen:
                stack.pop()
            else:
                next_visit = random.choice(unseen)
                self.remove_wall(x, y, next_visit[2])
                seen.add((next_visit[0], next_visit[1]))
                stack.append((next_visit[0], next_visit[1]))

    def solve(
            self,
            entry: tuple[int, int],
            exit: tuple[int, int]
    ) -> list[str] | None:
        seen: set[tuple[int, int]] = {entry}
        queue: deque[tuple[int, int]] = deque()
        queue.append(entry)
        came_from: dict[
            tuple[int, int],
            tuple[int, int, str]
        ] = {}
        found: bool = False
        while queue:
            current = queue.popleft()
            if current == exit:
                found = True
                break
            x, y = current
            for neighbor in self.get_neighbors(x, y):
                if self.has_wall(x, y, neighbor[2]) is False:
                    if (neighbor[0], neighbor[1]) not in seen:
                        seen.add((neighbor[0], neighbor[1]))
                        came_from[neighbor[0], neighbor[1]] = (
                            x, y, neighbor[2])
                        queue.append((neighbor[0], neighbor[1]))
        if not found:
            return None
        path = []
        node = exit
        while node != entry:
            x_prev, y_prev, Dir = came_from[node]
            path.append(Dir)
            node = (x_prev, y_prev)
        path = path[::-1]
        return path

    def get_path_coords(self, path: list[str] | None,
                        entry: tuple[int, int]) -> set[tuple[int, int]]:
        if path is None:
            return set()
        x, y = entry
        coords: set[tuple[int, int]] = {(x, y)}
        for direction in path:
            dx, dy = bible[direction][0], bible[direction][1]
            x += dx
            y += dy
            coords.add((x, y))
        return coords

    def make_pattern_anchors(self) -> set[tuple[int, int]]:
        ax: int = (self.width - 7) // 2
        ay: int = (self.height - 5) // 2

        blocked = []
        for j, row in enumerate(pattern_42):
            for i, is_blocked in enumerate(row):
                if is_blocked:
                    blocked.append((ax + i, ay + j))
        return set(blocked)

    def is_3x3_open(self, x: int, y: int) -> bool:
        for j in range(3):
            for i in range(2):
                if self.has_wall(x + i, y + j, "E"):
                    return False
        for j in range(2):
            for i in range(3):
                if self.has_wall(x + i, y + j, "N"):
                    return False
        return True

    # Temporary check (maybe)
    # This mf gets expensive in terms of performence for very large mazes
    def has_3x3_open(self) -> bool:
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                if self.is_3x3_open(x, y):
                    return True
        return False

    # Apparently very VERY bad practice to use mutable
    # (list, dict, set, ...) default args
    # Using has_wall() to reduce calls to has_3x3_open()
    def carve_unperfect_maze(self, entry: tuple[int, int], seed: int | None,
                             blocked: set[tuple[int, int]] | None = None,
                             loop_factor: float = 0.3) -> None:
        if blocked is None:
            blocked = set()
        dirs: list[str] = ["N", "E"]
        self.carve_maze(entry, seed, blocked)
        for x in range(self.width):
            for y in range(self.height):
                for direction in dirs:
                    if random.random() < loop_factor:
                        if self.has_wall(x, y, direction):
                            self.remove_wall(x, y, direction)
                            if self.has_3x3_open():
                                self.add_wall(x, y, direction)
