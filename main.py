from flask import Flask, render_template
from database.connection import close_db_connection, init_db
from routes.students import students_bp
import os

app = Flask(__name__)

# Conectamos las rutas del examen
app.register_blueprint(students_bp)

# Cerramos las conexiones de base de datos automáticamente al terminar cada petición
app.teardown_appcontext(close_db_connection)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    if not os.path.exists("students.db"):
        init_db(app)
        print("Base de datos 'students.db' creada e inicializada.")
        
    app.run(debug=True, port=5000)