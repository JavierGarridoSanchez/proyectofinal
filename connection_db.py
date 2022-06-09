import sqlite3
from sqlite3.dbapi2 import Connection


class ConnectionDB:

    def __init__(self):
        self.my_connection = sqlite3.connect("bd/juegonieve")
        self.my_cursor = self.my_connection.cursor()
