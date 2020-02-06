import sqlalchemy as db
import pymysql

pymysql.install_as_MySQLdb()

engine = db.create_engine("mysql://default:default@localhost:3306/todo")  # sqlalchemy.exc.OperationalError

connection = engine.connect()
metadata = db.MetaData()

table = db.Table("todo_lists", metadata, autoload=True, autoload_with=engine)

query = db.select([table])

result_proxy = connection.execute(query)

result_set = result_proxy.fetchall()

print(result_set)
