from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SQLTodoList(Base):
    __tablename__ = "todo_lists"

    list_id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR)
    description = Column(VARCHAR)
    hex_color = Column(VARCHAR)
    created_at = Column(TIMESTAMP)
