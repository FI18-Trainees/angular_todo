import json
import os

import sqlalchemy as db
import pymysql

from utils import Console

SHL = Console("DB_Connector")

pymysql.install_as_MySQLdb()

CONFIG_PATH = os.path.join("app", "db_connector", "connection.json")
with open(CONFIG_PATH, 'r', encoding="utf-8") as c:
    data = json.load(c)
try:
    connection_string = data["connection_string"]
except KeyError:
    SHL.error(f"connection string not found. Cannot connect to database.")


class DatabaseConnection:
    def __init__(self):
        SHL.info(f"Setting up database connection.")
        try:
            self.engine = db.create_engine(connection_string)
        except Exception:
            SHL.error(f"Could not connect to database.")
