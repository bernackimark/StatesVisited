from dataclasses import dataclass, field
from datetime import datetime

from controller.state import State
from db_layer.db import get_db_session
from db_layer.models import User
from sqlalchemy.orm.attributes import flag_modified  # notifies SQLAlchemy of an update to a JSON column


@dataclass
class UserStateRecord:
    """Represents the value for each state key in user.states."""
    visited_on: int = None
    visited_with: set = field(default_factory=set)
    added_on: str = datetime.now().isoformat()
    lmt: str = datetime.now().isoformat()


def add_user_state(u: User, state: State, yr: int = None, visited_with: set = None):
    """Merges the existing JSON data from the db_layer with another dictionary."""
    with get_db_session() as s:
        existing_record = s.get(User, u.email)
        if not existing_record:
            return
        new_state = {state.code: UserStateRecord(yr, visited_with).__dict__}
        updated = existing_record.states | new_state
        existing_record.states = updated
        s.commit()

def delete_user_state(u: User, state: State):
    """Removes a key-value from the JSON data column in the db_layer"""
    with get_db_session() as s:
        existing_record = s.get(User, u.email)
        del existing_record.states[state.code]
        flag_modified(existing_record, "states")  # Notify SQLAlchemy of the change
        s.commit()
