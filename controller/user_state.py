from dataclasses import dataclass
from datetime import datetime

from controller.state import State
from controller.user import User
from db.db import get_db_session
from db.models import UserState
from sqlalchemy.orm.attributes import flag_modified  # notifies SQLAlchemy of an update to a JSON column


@dataclass
class UserStateRecord:
    visited_on: int = None
    added_on: str = datetime.now().isoformat()
    lmt: str = datetime.now().isoformat()


def add_user_state(u: User, state: State, yr: int = None):
    """Merges the existing JSON data from the db with another dictionary."""
    with get_db_session() as s:
        existing_record = s.query(UserState).filter(UserState.user_id == u.id).first()
        if not existing_record:
            return
        new_state = {state.code: UserStateRecord(yr).__dict__}
        updated = existing_record.data | new_state
        existing_record.data = updated
        s.commit()

def delete_user_state(u: User, state: State):
    """Removes a key-value from the JSON data column in the db"""
    with get_db_session() as s:
        existing_record = s.query(UserState).filter(UserState.user_id == u.id).first()
        del existing_record.data[state.code]
        flag_modified(existing_record, "data")  # Notify SQLAlchemy of the change
        s.commit()
