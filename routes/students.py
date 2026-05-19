# Importando librerias necesarias

from flask import Blueprint, request, jsonify, render_template # Importamos Blueprint para crear un módulo de rutas, request para manejar las solicitudes HTTP, jsonify para devolver respuestas JSON y render_template para servir plantillas HTML
from database.connection import get_db_connection # Importamos la función para obtener la conexión a la base de datos
import sqlite3 # Importamos sqlite3 para manejar errores de integridad y otras operaciones relacionadas con la base de datos
from datetime import datetime # Importamos datetime para manejar las fechas de creación y actualización de los estudiantes

students_bp = Blueprint("students", __name__) # Creamos un blueprint llamado "students" para organizar las rutas relacionadas con los estudiantes


def serialize_student(row): # Función para convertir una fila de la base de datos en un diccionario serializable a JSON
    return {
        "id": row["id"],                           # Incluimos el ID del estudiante en la respuesta JSON
        "dni": row["dni"],                         # Incluimos el DNI del estudiante en la respuesta JSON
        "name": row["name"],                       # Incluimos el nombre del estudiante en la respuesta JSON
        "age": row["age"],                         # Incluimos la edad del estudiante en la respuesta JSON
        "grade": row["grade"],                     # Incluimos la nota del estudiante en la respuesta JSON
        "is_approved": bool(row["is_approved"]),    # Convertimos el valor de is_approved a booleano para que sea más legible en la respuesta JSON
        "created_at": row["created_at"],             # Incluimos la fecha de creación del estudiante en la respuesta JSON
        "updated_at": row["updated_at"],           # Incluimos la fecha de última actualización del estudiante en la respuesta JSON
    }


# 1. Creando un estudiante con (POST /students)


@students_bp.route("/students", methods=["POST"])
def create_student():
    data = request.get_json() or {}
    if (
        not data.get("dni")
        or not data.get("name")
        or data.get("age") is None
        or data.get("grade") is None
        or data.get("is_approved") is None
    ):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO students (dni, name, age, grade, is_approved) VALUES (?, ?, ?, ?, ?)",
            (
                data["dni"],
                data["name"],
                int(data["age"]),
                float(data["grade"]),
                bool(data["is_approved"]),
            ),
        )
        conn.commit()
        cur.execute("SELECT * FROM students WHERE id = ?", (cur.lastrowid,))
        return jsonify(serialize_student(cur.fetchone())), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El DNI ya se encuentra registrado"}), 400


# 2. Obtener todos los estudiantes con (GET /students)

@students_bp.route("/students", methods=["GET"])
def get_all_students():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    return jsonify([serialize_student(row) for row in rows]), 200


# 3. Obtener un estudiante por ID con (GET /students/<id>)
@students_bp.route("/students/<int:student_id>", methods=["GET"])
def get_student_by_id(student_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cur.fetchone()
    if row is None:
        return jsonify({"error": "Estudiante no encontrado"}), 404
    return jsonify(serialize_student(row)), 200


# 4. Actualizar un estudiante con (PUT/PATCH /students/<id>)
@students_bp.route("/students/<int:student_id>", methods=["PUT", "PATCH"])
def update_student(student_id):
    data = request.get_json() or {}
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cur.fetchone()
    if student is None:
        return jsonify({"error": "Estudiante no encontrado"}), 404

    dni = data.get("dni", student["dni"])
    name = data.get("name", student["name"])
    age = data.get("age", student["age"])
    grade = data.get("grade", student["grade"])
    is_approved = data.get("is_approved", student["is_approved"])
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cur.execute(
            """
            UPDATE students 
            SET dni = ?, name = ?, age = ?, grade = ?, is_approved = ?, updated_at = ?
            WHERE id = ?
        """,
            (
                dni,
                name,
                int(age),
                float(grade),
                bool(is_approved),
                current_time,
                student_id,
            ),
        )
        conn.commit()
        cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        return jsonify(serialize_student(cur.fetchone())), 200
    except sqlite3.IntegrityError:
        return jsonify(
            {"error": "No se pudo actualizar. El DNI ya pertenece a otro estudiante"}
        ), 400


# 5. Eliminar un estudiante con (DELETE /students/<id>)

@students_bp.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    if cur.fetchone() is None:
        return jsonify({"error": "Estudiante no encontrado"}), 404

    cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    return jsonify({"message": f"Estudiante con ID {student_id} eliminado"}), 200


# 6. Creación masiva / Bulk insert con (POST /students/bulk)

@students_bp.route("/students/bulk", methods=["POST"])
def bulk_insert_students():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "El cuerpo debe ser una lista"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    inserted_count = 0
    try:
        for item in data:
            if (
                not item.get("dni")
                or not item.get("name")
                or item.get("age") is None
                or item.get("grade") is None
                or item.get("is_approved") is None
            ):
                continue
            cur.execute(
                "INSERT INTO students (dni, name, age, grade, is_approved) VALUES (?, ?, ?, ?, ?)",
                (
                    item["dni"],
                    item["name"],
                    int(item["age"]),
                    float(item["grade"]),
                    bool(item["is_approved"]),
                ),
            )
            inserted_count += 1
        conn.commit()
        return jsonify(
            {"message": f"Bulk insert completado. {inserted_count} agregados."}
        ), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Error de duplicidad de DNI en la lista masiva"}), 400


# 7. Promedio de notas con (GET /students/average)

@students_bp.route("/students/average", methods=["GET"])
def get_students_average():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT AVG(grade) as promedio FROM students")
    result = cur.fetchone()
    promedio = result["promedio"] if result["promedio"] is not None else 0.0
    return jsonify({"average_grade": round(promedio, 2)}), 200


# 8. Renderizar tabla HTMX (GET /students/table)

@students_bp.route("/students/table", methods=["GET"])
def get_students_html_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    return render_template("partials/students_table.html", student_list=rows)
