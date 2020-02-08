from typing import List, Optional
from contextlib import contextmanager

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import NoResultFound

from .db_connector import DatabaseConnection
from app.obj import Todo, TodoList, CreationError, SQLTodo, SQLTodoList, DatabaseError
from utils import Console

SHL = Console("DatabaseInterface")


class TodoListSelectAll(object):
    def go(self, session) -> List[SQLTodoList]:
        return session.query(SQLTodoList)


class TodoListSelectByListId(object):
    def go(self, session, list_id: int) -> SQLTodoList:
        return session.query(SQLTodoList).filter(SQLTodoList.list_id == list_id).one()


class TodoListInsertOrUpdate(object):
    def go(self, session, obj):
        return session.merge(obj)


class TodoSelectAll(object):
    def go(self, session) -> List[SQLTodoList]:
        return session.query(SQLTodo)


class TodoSelectByListId(object):
    def go(self, session, list_id: int) -> List[SQLTodoList]:
        return session.query(SQLTodo).filter(SQLTodo.list_id == list_id).all()


class TodoSelectByItemId(object):
    def go(self, session, item_id: int) -> SQLTodoList:
        return session.query(SQLTodo).filter(SQLTodo.item_id == item_id).one()


class TodoInsertOrUpdate(object):
    def go(self, session, obj):
        return session.merge(obj)


class __DatabaseInterface:
    def __init__(self):
        self.db = DatabaseConnection()

    @contextmanager
    def session_scope(self):
        session = scoped_session(sessionmaker(bind=self.db.engine, expire_on_commit=False))
        try:
            yield session
            session.commit()
        except DatabaseError as e:
            session.rollback()
            raise DatabaseError(e)
        except NoResultFound as e:
            session.rollback()
            raise NoResultFound()
        except Exception as e:
            SHL.error(f"Error in db session. {e}")
            session.rollback()
            raise DatabaseError(e)
        finally:
            session.close()

    def todo_list_select_all(self) -> List[TodoList]:
        SHL.info(f"Selecting all entries of TodoList table.")
        with self.session_scope() as session:
            try:
                for e in TodoListSelectAll().go(session):
                    try:
                        yield TodoList(e)
                    except CreationError:
                        continue
            except OperationalError as e:
                SHL.error(f"Error in db session. {e}")
                raise DatabaseError(e)
            return []

    def todo_list_select_by_list_id(self, list_id: int) -> Optional[TodoList]:
        SHL.info(f"Selecting all entries of TodoList table with list_id '{list_id}'.")
        with self.session_scope() as session:
            try:
                return TodoList(TodoListSelectByListId().go(session, list_id=list_id))
            except OperationalError as e:
                SHL.error(f"Error in db session. {e}")
                raise DatabaseError(e)
            except NoResultFound as e:
                SHL.error(f"Error in db session. {e}")
                raise NoResultFound()
            except CreationError:
                return

    def todo_list_insert_or_update(self, obj):
        if isinstance(obj, TodoList):
            obj = obj.to_sql_obj()
        SHL.info(f"Inserting/Updating data in TodoList table.")
        with self.session_scope() as session:
            try:
                return TodoListInsertOrUpdate().go(session, obj=obj)
            except OperationalError as e:
                SHL.error(f"Error in db session. {e}")
                raise DatabaseError(e)

    def todo_select_all(self) -> List[TodoList]:
        SHL.info(f"Selecting all entries of Todo table.")
        with self.session_scope() as session:
            try:
                for e in TodoSelectAll().go(session):
                    try:
                        yield TodoList(e)
                    except CreationError:
                        continue
            except OperationalError as e:
                SHL.error(f"Error in db session. {e}")
                raise DatabaseError(e)
            return []

    def todo_select_by_list_id(self, list_id: int) -> List[TodoList]:
        SHL.info(f"Selecting all entries of Todo table with list_id '{list_id}'.")
        with self.session_scope() as session:
            try:
                for e in TodoSelectByListId().go(session, list_id=list_id):
                    try:
                        yield Todo(e)
                    except CreationError:
                        continue
            except OperationalError as e:
                SHL.error(f"Error in db session. {e}")
                raise DatabaseError(e)
            except NoResultFound as e:
                SHL.error(f"Error in db session. {e}")
                raise NoResultFound()
            except CreationError:
                return

    def todo_select_by_item_id(self, item_id: int) -> Optional[Todo]:
        SHL.info(f"Selecting all entries of Todo table with item_id '{item_id}'.")
        with self.session_scope() as session:
            try:
                return Todo(TodoSelectByItemId().go(session, item_id=item_id))
            except OperationalError as e:
                SHL.error(f"Error in db session. {e}")
                raise DatabaseError(e)
            except NoResultFound as e:
                SHL.error(f"Error in db session. {e}")
                raise NoResultFound()
            except CreationError:
                return

    def todo_insert_or_update(self, obj):
        if isinstance(obj, TodoList):
            obj = obj.to_sql_obj()
        SHL.info(f"Inserting/Updating data in Todo table.")
        with self.session_scope() as session:
            try:
                return TodoInsertOrUpdate().go(session, obj=obj)
            except OperationalError as e:
                SHL.error(f"Error in db session. {e}")
                raise DatabaseError(e)


db_interface = __DatabaseInterface()
