import sqlite3           # Importamos el módulo sqlite3 para trabajar con la base de datos SQLite
from flask import g      # Importamos "g" de Flask, que es un espacio de almacenamiento para datos específicos de cada solicitud, útil para almacenar la conexión a la base de datos durante la vida de una solicitud

DATABASE_NAME = "students.db"          # Definimos el nombre del archivo de la base de datos SQLite

def get_db_connection():                          # Obtenemos la conexión a la base de datos desde el objeto "g" de Flask, que es un espacio de almacenamiento para datos específicos de cada solicitud. Si no existe una conexión, se crea una nueva y se almacena en "g" para reutilizarla durante la misma solicitud
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_NAME)       # Establecemos la conexión a la base de datos SQLite utilizando el nombre del archivo definido en DATABASE_NAME
        g.db.row_factory = sqlite3.Row  
    return g.db

def close_db_connection(exception=None):           # Cerramos la conexión a la base de datos al finalizar cada petición para liberar recursos
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db(app):                                  # Inicializamos la base de datos ejecutando el script SQL para crear las tablas necesarias
    with app.app_context():
        db = sqlite3.connect(DATABASE_NAME)
        with open("schema.sql", "r") as f:
            db.executescript(f.read())
        db.close()                                 # Cerramos la conexión a la base de datos después de inicializarla