import sqlite3
from flask import g

DATABASE_NAME = "students.db"

def get_db_connection():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_NAME)
        g.db.row_factory = sqlite3.Row  
    return g.db

def close_db_connection(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = sqlite3.connect(DATABASE_NAME)
        with open("schema.sql", "r") as f:
            db.executescript(f.read())
        db.close()