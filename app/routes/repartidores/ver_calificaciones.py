from flask import Blueprint, render_template
from app.db import conexion  

calificaciones_bp = Blueprint('calificaciones', __name__)

@calificaciones_bp.route('/', methods=['GET'])  # Cambiado a '/' para que coincida con el prefijo registrado en create_app()
def ver_calificaciones():
    conn = conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM calificaciones")
            calificaciones = cursor.fetchall()
    finally:
        conn.close()

    return render_template('repartidores/ver_calificaciones.html', calificaciones=calificaciones)  # Asegúrate de pasar las calificaciones a la plantilla