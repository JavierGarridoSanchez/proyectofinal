from connection_db import ConnectionDB

from scoreboard_dao import ScoreBoardDao


class ScoreBoardDaoImple(ScoreBoardDao):

    def __init__(self):
        self.connection = ConnectionDB()

    def insert_player(self, markers):
        jugadores = [markers.name_surname, markers.score, markers.kills, markers.coins, markers.level]
        self.connection = ConnectionDB()
        self.connection.my_cursor.execute("INSERT INTO WIN VALUES(?,?,?,?,?)", jugadores)
        self.connection.my_connection.commit()
        self.connection.my_connection.close()

    def insert_default_players(self):
        players = [
            ('Alfonso Gutierrez', 45, 2, 44, 0),
            ('Garcia Lorca', 30, 3, 60, 0),
            ('Jaime Roldan', 42, 1, 14, 0)
        ]
        try:
            self.connection.my_cursor.executemany("INSERT INTO WIN VALUES(?,?,?,?,?)", players)
            self.connection.my_connection.commit()
            self.connection.my_connection.close()

        except Exception:
            print(Exception)

    def read_players(self):
        self.connection = ConnectionDB()
        self.connection.my_cursor.execute("SELECT * FROM WIN")

        player = self.connection.my_cursor.fetchall()  # devuelve lista con los registros de el cursor
        self.connection.my_connection.close()
        return player

    def read_player(self, name_surname):
        self.connection = ConnectionDB()
        sql_update_query = "SELECT * FROM WIN WHERE NOMBRE_APELLIDO = ?"
        self.connection.my_cursor.execute(sql_update_query, (name_surname,))
        registros = self.connection.my_cursor.fetchall()
        # he cambiado el for con return de registros que iba aqui
        self.connection.my_connection.commit()
        self.connection.my_connection.close()
        for d in registros:
            return d

    def delete_player(self, player):
        self.connection = ConnectionDB()
        sql_update_query = "DELETE FROM WIN WHERE NOMBRE_APELLIDO = ?"
        self.connection.my_cursor.execute(sql_update_query, (player,))
        self.connection.my_connection.commit()
        self.connection.my_connection.close()

    def get_player_level(self, player):
        self.connection = ConnectionDB()
        sql_update_query = "SELECT NIVEL FROM WIN WHERE NOMBRE_APELLIDO = ?"
        self.connection.my_cursor.execute(sql_update_query, (player,))
        registros = self.connection.my_cursor.fetchall()
        # he cambiado el for con return de registros que iba aqui
        self.connection.my_connection.commit()
        self.connection.my_connection.close()
        for d in registros:
            return d

    def top_players(self):
        self.connection = ConnectionDB()
        self.connection.my_cursor.execute("SELECT * FROM WIN ORDER BY COINS DESC LIMIT 10")

        player = self.connection.my_cursor.fetchall()  # devuelve lista con los registros de el cursor
        self.connection.my_connection.close()
        return player
