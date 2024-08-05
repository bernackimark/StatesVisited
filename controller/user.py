from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from db.db import get_db_session
from db.models import User as UserTable, UserState as UserStateTable

PWORD_PLACEHOLDER = 'abc123'


@dataclass
class User:
    id: uuid4
    email: str
    name: str
    home_state_code: str
    hashed_password: str
    state_data: dict
    is_active: bool = True
    last_login: datetime = datetime.now()

    def __post_init__(self):
        if not self.state_data:
            self.state_data = {}

    @property
    def state_count(self) -> int:
        return len(self.state_data)


def create_user(email: str, name: str, home_state_code: str) -> int | None:
    """Creates a record in both the user & user_state tables.
    If the user already exists, None is returned.  If a user is created, 1 is returned."""
    user = UserTable(email=email, name=name, home_state_code=home_state_code, hashed_password=PWORD_PLACEHOLDER)

    with get_db_session() as s:
        already_exists = s.query(UserTable).filter(UserTable.email == email).one_or_none()
        if already_exists:
            return None

        s.add(user)
        s.commit()
        user_id = s.query(UserTable.id).filter(UserTable.email == email).scalar()
        user_state = UserStateTable(user_id=user_id, data={})
        s.add(user_state)
        s.commit()
        return 1

def modify_user(user_id: int, name: str, home_state_code: str):
    with get_db_session() as s:
        user = s.query(UserTable).get(user_id)
        user.name = name
        user.home_state_code = home_state_code
        s.commit()

def get_user(user_id: int) -> User | None:
    with get_db_session() as s:
        data = s.query(UserTable, UserStateTable).filter(UserTable.id == UserStateTable.user_id,
                                                         UserTable.id == user_id).one_or_none()
        if data:
            u, us = data
            return User(u.id, u.email, u.name, u.home_state_code, u.hashed_password, us.data, u.is_active, u.last_login)

