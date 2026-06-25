import sys
from dataclasses import dataclass


@dataclass
class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool


def read_config() -> dict[str, str]:
    if len(sys.argv) != 2:
        print("Error: Please input the name of a Configuration File")
        return {'error': "arg count"}
    result: dict[str, str] = {}
    filename: str = sys.argv[1]
    try:
        with open(filename) as fd:
            tmp_content = fd.read()
    except FileNotFoundError as e:
        print("File does not exist.")
        return {'error': str(e)}
    except OSError as e:
        print(e)
        return {'error': str(e)}
    content = tmp_content.splitlines()
    for line in content:
        stripped = line.strip()
        if not stripped or stripped[0] == "#":
            continue
        pairs: list[str] = stripped.split("=")
        if len(pairs) != 2:
            er: str = "irregular number of '=' symbols on a single line "
            print(f"Error: {er}")
            return {'error': er}
        key: str = pairs[0].strip()
        value: str = pairs[1].strip()
        result[key] = value
    return result


def verify_file(file: dict[str, str]) -> Config | None:
    look_for: list[str] = ["WIDTH", "HEIGHT",
                           "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    if "error" in file:
        return None
    for a in look_for:
        if a not in file.keys():
            print(f"ERROR: {a} was not found in the config file")
            return None
    try:
        x_width: int = int(file["WIDTH"])
        y_height: int = int(file["HEIGHT"])
    except ValueError as e:
        print(e)
        return None
    if x_width <= 0 or y_height <= 0:
        print("Invalid Dimensions")
        return None
    try:
        entry: str = file["ENTRY"]
        exit: str = file["EXIT"]
        x_entry, y_entry = map(int, entry.split(","))
        x_exit, y_exit = map(int, exit.split(","))
    except ValueError as e:
        print(e)
        return None
    if not (0 <= x_entry < x_width and 0 <= y_entry < y_height):
        print("Entry coordinates are Invalid")
        return None
    if not (0 <= x_exit < x_width and 0 <= y_exit < y_height):
        print("Exit coordinates are Invalid")
        return None
    if x_entry == x_exit and y_entry == y_exit:
        print("Error: exit and entry points cannot coincide")
        return None
    if file["PERFECT"].strip().lower() == "true":
        perfect_status: bool = True
    elif file["PERFECT"].strip().lower() == "false":
        perfect_status = False
    else:
        print("Error: Perfect Status could not be confirmed")
        return None
    if not file["OUTPUT_FILE"]:
        print("ERROR: Output file cannot be empty")
        return None
    config: Config = Config(
        width=x_width,
        height=y_height,
        entry=(x_entry, y_entry),
        exit=(x_exit, y_exit),
        output_file=file["OUTPUT_FILE"],
        perfect=perfect_status
    )
    return config
