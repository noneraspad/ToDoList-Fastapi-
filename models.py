from sqlalchemy import Boolean, Column, Integer, String, DateTime

from database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    complete = Column(Boolean, default=False)
    date = Column(String)
    times = Column(String)
