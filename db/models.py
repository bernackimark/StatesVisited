from sqlalchemy import Column, DateTime, Integer, JSON, String, Boolean, ForeignKey, UUID, func
from sqlalchemy.orm import relationship
from .db import Base, engine

class User(Base):
    __tablename__ = "sv_user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    home_state_code = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, default=func.now(), onupdate=func.now())

    states = relationship("UserState", back_populates="user")

class UserState(Base):
    __tablename__ = "sv_user_state"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("sv_user.id"))
    data = Column(JSON)

    user = relationship("User", back_populates="states")


if __name__ == '__main__':
    if input('Are you sure you want to crete all tables? (Y/n) ') == 'Y':
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print('All tables dropped and recreated successfully')
