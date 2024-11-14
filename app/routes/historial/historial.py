from flask import Blueprint, render_template
from app.db import conexion

historial_bp = Blueprint('historial', __name__)

@historial_bp.route('/ver', methods=['GET'])
def ver_historial():
    conn = conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM historialpedidos")
            historial = cursor.fetchall()
    finally:
        conn.close()

    return render_template('historial/ver_historial.html', historial=historial)

