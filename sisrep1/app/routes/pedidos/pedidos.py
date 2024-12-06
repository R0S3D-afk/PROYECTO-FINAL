from flask import Blueprint, render_template
from flask_login import login_required, current_user  # Importar current_user
from app.db import conexion

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')

# Ruta para ver los pedidos del cliente
@pedidos_bp.route('/')
@login_required
def mostrar_pedidos():
    conn = conexion()
    pedidos = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, direccion_entrega, contenido, urgencia, estado, fecha_pedido FROM pedidos WHERE id_cliente = %s", (current_user.id,))
            pedidos = cursor.fetchall()  # Solo obtiene los pedidos del cliente autenticado
    finally:
        conn.close()
    return render_template('pedidos/ver_pedidos.html', pedidos=pedidos)