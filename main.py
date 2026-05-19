from flask import Flask, render_template # Importamos render_template para servir la página HTML
from database.connection import close_db_connection, init_db # Importamos las funciones para manejar la base de datos
from routes.students import students_bp # Importamos el blueprint de estudiantes para registrarlo en la aplicación principal
import os

app = Flask(__name__) # Creamos la aplicación Flask

# Conectamos el blueprint de estudiantes a la aplicación principal

app.register_blueprint(students_bp)

# Cerramos las conexiones de base de datos automáticamente al terminar cada petición

app.teardown_appcontext(close_db_connection)

@app.route("/") # Ruta para servir la página HTML principal
def index():
    return render_template("index.html")

if __name__ == "__main__":
    if not os.path.exists("students.db"):
        init_db(app)
        print("Base de datos 'students.db' creada e inicializada.")
        
    app.run(debug=True, port=5005) # Ejecutamos la aplicación en modo debug en el puerto 5005