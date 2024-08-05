from dataclasses import dataclass, field

from db.db import get_db_session
from db.models import User as UserTable, UserState as UserStateTable


def get_all_data() -> "Data":
    with get_db_session() as s:
        data = s.query(UserTable.name, UserTable.home_state_code,
                       UserStateTable.data).filter(UserTable.id == UserStateTable.user_id).all()
    all_data = []
    for name, home_state, states in data:
        visited = [VisitedState(code, d['visited_on'], d['added_on']) for code, d in states.items()]
        all_data.append(DataRow(name, home_state, visited))
    return Data(all_data)

@dataclass
class VisitedState:
    state_code: str
    year: int
    added_on: str

@dataclass
class DataRow:
    """An object with user's name, user home state code, and a list of visited states"""
    name: str
    home_state_code: str
    visited_states: list[VisitedState]

    @property
    def state_cnt(self) -> int:
        return len(self.visited_states)

@dataclass
class Data:
    """A list of data rows, on which to filter & group data"""
    data: list[DataRow] = field(default_factory=get_all_data)

    @property
    def users(self) -> list[str]:
        return sorted([r.name for r in self.data])

    @property
    def users_and_state_counts(self) -> list[dict[str: int]]:
        return [{'name': r.name, 'home_state': r.home_state_code, 'state_cnt': r.state_cnt} for r in self.data]
