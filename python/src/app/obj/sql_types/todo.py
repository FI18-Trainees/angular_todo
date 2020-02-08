from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SQLTodo(Base):
    __tablename__ = "todos"

    item_id = Column(INTEGER, primary_key=True)
    list_id = Column(INTEGER)
    title = Column(VARCHAR)
    description = Column(VARCHAR)
    finished = Column(INTEGER)
    due_date = Column(TIMESTAMP)
    address = Column(TEXT)
    priority = Column(INTEGER)
    subtasks = Column(TEXT)
    reminder = Column(TIMESTAMP)
