from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import conexion

pedidos_bp = Blueprint('pedidos', __name__)

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

@pedidos_bp.route('/crear', methods=['GET', 'POST'])
def crear_pedido():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        direccion_entrega = request.form['direccion_entrega']
        contenido = request.form['contenido']
        urgencia = request.form['urgencia']
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO pedidos (id_cliente, direccion_entrega, contenido, urgencia) VALUES (%s, %s, %s, %s)",
                               (id_cliente, direccion_entrega, contenido, urgencia))
            conn.commit()
            flash('Pedido creado exitosamente', 'success')
            return redirect(url_for('pedidos.mostrar_pedidos'))
        finally:
            conn.close()
    return render_template('pedidos/crear_pedidos.html')
