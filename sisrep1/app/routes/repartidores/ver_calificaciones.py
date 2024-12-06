from flask import Blueprint, render_template
from app.db import conexion

calificaciones_bp = Blueprint('calificaciones', __name__)

# Ruta para ver las calificaciones de un repartidor
@calificaciones_bp.route('/calificaciones/<int:id_repartidor>')
def ver_calificaciones(id_repartidor):
    conn = conexion()
    try:
        with conn.cursor() as cursor:
            # Consulta para obtener todas las calificaciones de un repartidor específico
            cursor.execute("""
                SELECT c.id, c.calificacion, c.comentario, c.fecha, u.nombre
                FROM calificaciones c
                JOIN usuarios u ON c.id_cliente = u.id
                WHERE c.id_repartidor = %s
            """, (id_repartidor,))
            calificaciones = cursor.fetchall()
    finally:
        conn.close()

    return render_template('repartidores/ver_calificaciones.html', calificaciones=calificaciones)