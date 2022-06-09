from connection_db import ConnectionDB

connection = ConnectionDB()  # instancia para crear la base de datos
try:
    connection.my_cursor.execute('''
            CREATE TABLE win (
            NOMBRE_APELLIDO VARCHAR(50) PRIMARY KEY,
            PUNTUACION INTEGER,
            KILLS INTEGER,
            COINS INTEGER,
            NIVEL INTEGER)
        ''')

    connection.my_connection.commit()
except:
    pass

connection.my_connection.close()
