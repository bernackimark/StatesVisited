from dataclasses import dataclass

from db.db import get_db_session
from db.models import User as UserTable, UserState as UserStateTable


@dataclass
class VisitedState:
    """Each state from the array of states from the db user_state.data column (JSON)"""
    state_code: str
    year: int
    added_on: str

@dataclass
class DataRow:
    """A convenience object with select elements from the user & user_state tables"""
    user_id: int
    name: str
    home_state_code: str
    state_data: list[VisitedState]

    @property
    def state_cnt(self) -> int:
        return len(self.state_data)


def get_all_data() -> list[DataRow]:
    """Get all db records, joining user & user_state & returning some of the columns"""
    with get_db_session() as s:
        data = s.query(UserTable.id, UserTable.name, UserTable.home_state_code,
                       UserStateTable.data).filter(UserTable.id == UserStateTable.user_id).all()
    all_data = []
    for user_id, name, home_state, states in data:
        visited = [VisitedState(code, d['visited_on'], d['added_on']) for code, d in states.items()]
        all_data.append(DataRow(user_id, name, home_state, visited))
    return all_data
