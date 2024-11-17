from flask import Blueprint, render_template
from app.db import conexion

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')

@pedidos_bp.route('/')
def mostrar_pedidos():
    conn = conexion()
    pedidos = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, id_cliente, direccion_entrega, contenido, urgencia, estado, fecha_pedido FROM pedidos")
            pedidos = cursor.fetchall()
    finally:
        conn.close()
    return render_template('pedidos/ver_pedidos.html', pedidos=pedidos)
