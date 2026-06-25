import random
from collections import deque

bible: dict[str, tuple[int, int, int, int]] = {
    "N": (0, 1, 1, 4),
    "E": (1, 0, 2, 8),
    "S": (0, -1, 4, 1),
    "W": (-1, 0, 8, 2),
}

pattern_42: list[list[int]] = [
    [0, 1, 0, 1, 1, 1],
    [0, 1, 0, 1, 0, 0],
    [1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1]
]


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.height = height
        self.width = width
        self.storage: list[list[int]] = [
            [15 for _ in range(width)] for _ in range(height)]

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def has_wall(self, x: int, y: int, direction: str) -> bool | None:
        book = {
            "N": 1,
            "E": 2,
            "S": 4,
            "W": 8,
        }
        bi_direction: int | None = book.get(direction, None)
        if bi_direction is None:
            print("ERROR: Unknown Direction")
            return None
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
            print("Error: Invalid Direction")
            return
        neigh_info: tuple[int, int, int, int] = bible[direction]
        dx: int = neigh_info[0]
        dy: int = neigh_info[1]
        b1: int = neigh_info[2]
        b2: int = neigh_info[3]
        if (x + dx, y + dy, direction) not in valid:
            print("Error: Cannot remove outer maze walls")
            return
        else:
            self.storage[y][x] &= ~b1
            self.storage[y + dy][x + dx] &= ~b2

    def carve_maze(
            self, entry: tuple[int, int], seed: int | None = None
    ) -> None:
        if seed is not None:
            random.seed(seed)
        seen: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []
        stack.append(entry)
        seen.add(entry)
        while stack:
            x, y = stack[-1]
            unseen = [i for i in self.get_neighbors(
                x, y) if (i[0], i[1]) not in seen]
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
