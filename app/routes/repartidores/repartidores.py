from flask import Blueprint, render_template
from app.db import conexion

repartidores_bp = Blueprint('repartidores', __name__)

@repartidores_bp.route('/', methods=['GET'])
def repartidores_db():
    conn = conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM repartidores")
            repartidores = cursor.fetchall()  # Recupera todos los repartidores
            print(repartidores)  # Imprime los resultados para depuración
    finally:
        conn.close()

    return render_template('repartidores/repartidores.html', repartidores=repartidores)