from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import conexion
from flask_login import current_user

crear_pedido_bp = Blueprint('crear_pedido', __name__, url_prefix='/pedidos')

# Ruta para crear un pedido
@crear_pedido_bp.route('/crear', methods=['GET', 'POST'])
def crear_pedido():
    if request.method == 'POST':
        direccion_entrega = request.form['direccion_entrega']
        contenido = request.form['contenido']
        urgencia = request.form['urgencia']
        id_cliente = current_user.id  # Usamos el id del cliente autenticado
        
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO pedidos (id_cliente, direccion_entrega, contenido, urgencia) VALUES (%s, %s, %s, %s)",
                    (id_cliente, direccion_entrega, contenido, urgencia)
                )
            conn.commit()
            flash('Pedido creado exitosamente', 'success')
        finally:
            conn.close()
        return redirect(url_for('pedidos.mostrar_pedidos'))  # Redirige a la vista de pedidos
    return render_template('pedidos/crear_pedidos.html')
