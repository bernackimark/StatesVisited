from dataclasses import dataclass, field
from datetime import datetime

from db_layer.db import get_db_session
from db_layer.models import User as UserTable


@dataclass
class User:
    email: str
    name: str
    home_state_code: str
    states: dict = field(default_factory=dict)

    @property
    def state_cnt(self) -> int:
        return len(self.states)

    def has_visited(self, state_code: str) -> bool:
        return state_code in self.states


def create_user(email: str, name: str, home_state_code: str) -> User | None:
    """Creates a record in both the user & table.
    If the user already exists, None is returned.  If a user is created, a User dataclass is returned."""
    user = UserTable(email=email, name=name, home_state_code=home_state_code)

    with get_db_session() as s:
        if s.get(UserTable, email):
            return None

        s.add(user)
        s.commit()
        return User(email=email, name=name, home_state_code=home_state_code, states={})

def modify_user(email: str, name: str, home_state_code: str):
    with get_db_session() as s:
        user = s.get(UserTable, email)
        user.name = name
        user.home_state_code = home_state_code
        s.commit()

def get_user(email: str) -> User | None:
    with get_db_session() as s:
        u: UserTable = s.get(UserTable, email)
        if not u:
            return None
        u.last_login = datetime.now()
        s.commit()
        return User(email=u.email, name=u.name, home_state_code=u.home_state_code, states=u.states)

def get_all_users() -> list[User]:
    """Get all is_active users from db, return User dataclass objects"""
    with get_db_session() as s:
        data = s.query(UserTable).filter(UserTable.is_active).all()
        return [User(email=r.email, name=r.name, home_state_code=r.home_state_code, states=r.states) for r in data]
