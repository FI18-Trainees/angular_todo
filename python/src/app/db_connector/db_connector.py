import json
import os

import sqlalchemy as db
import pymysql

from utils import Console, cfg

SHL = Console("DB_Connector")

pymysql.install_as_MySQLdb()

connection_string = cfg.get("connection_string")


class DatabaseConnection:
    def __init__(self):
        SHL.info(f"Setting up database connection.")
        try:
            self.engine = db.create_engine(connection_string)
        except Exception:
            SHL.error(f"Could not connect to database.")
