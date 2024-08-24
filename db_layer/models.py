from sqlalchemy import Column, DateTime, Integer, JSON, String, Boolean, func
from db_layer.db import Base, engine

class User(Base):
    __tablename__ = "sv_user"
    email = Column(String, primary_key=True, unique=True, index=True)
    name = Column(String, unique=True, nullable=False)
    home_state_code = Column(String)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, default=func.now(), onupdate=func.now())
    states = Column(JSON, default={})

    @property
    def k_v(self) -> dict:
        # the first entry in a Base instance dict is some sqlalchemy junk, hence  "idx > 0"
        return {k: v for idx, (k, v) in enumerate(self.__dict__.items()) if idx > 0}


if __name__ == '__main__':
    if input('Are you sure you want to crete all tables? (Y/n) ') == 'Y':
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print('All tables dropped and recreated successfully')
