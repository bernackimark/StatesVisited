from dataclasses import dataclass
import json
import pkgutil  # so that the json file within the same package can be read


@dataclass
class State:
    code: str
    name: str
    coord: tuple[int, int]


def states_list() -> list[State]:
    d: dict = json.loads(pkgutil.get_data(__package__, 'states.json'))
    return [State(code, name, (coord[0], coord[1])) for code, (name, coord) in d.items()]

def states_by_coord() -> dict[tuple[int, int]: State]:
    """Returns {(6, 6): State(code='AL', name='Alabama', (3, 2): State(code='WY', name='Wyoming', coord=(3, 2))}"""
    return {s.coord: s for s in states_list()}
