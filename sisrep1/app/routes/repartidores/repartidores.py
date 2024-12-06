from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app.models.repartidor import Repartidor
from app.models.pedido import Pedido

repartidores_bp = Blueprint('repartidores', __name__)


# Ruta para el perfil del repartidor (registrar o editar)
@repartidores_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    usuario_id = current_user.id
    repartidor = Repartidor.get_by_usuario_id(usuario_id)

    if request.method == 'POST':
        tipo_transporte = request.form['tipo_transporte']
        licencia = request.form['licencia']

        # Guardamos los datos del repartidor en la base de datos
        if Repartidor.create(usuario_id, tipo_transporte, licencia):
            return redirect(url_for('repartidores.panel'))  # Redirigir al panel

    return render_template('repartidores/perfil.html', repartidor=repartidor)


# Ruta para el panel principal del repartidor
@repartidores_bp.route('/panel')
@login_required
def panel():
    usuario_id = current_user.id
    repartidor = Repartidor.get_by_usuario_id(usuario_id)

    # Si no tiene perfil, lo redirigimos a completar perfil
    if not repartidor:
        return redirect(url_for('repartidores.perfil'))

    pedidos = Pedido.get_all()

    return render_template('repartidores/panel.html', pedidos=pedidos)




@repartidores_bp.route('/tomar_pedido/<int:pedido_id>')
@login_required
def tomar_pedido(pedido_id):
    try:
        usuario_id = current_user.id
        repartidor = Repartidor.get_by_usuario_id(usuario_id)

        # Verificar que el repartidor tenga un perfil antes de tomar el pedido
        if not repartidor:
            return redirect(url_for('repartidores.perfil'))

        # Intentamos actualizar el pedido y asignarlo al repartidor
        if Pedido.asignar_a_repartidor(pedido_id, repartidor.id):
            return redirect(url_for('repartidores.panel'))
        else:
            flash('Ocurrió un error al tomar el pedido.')
            return redirect(url_for('repartidores.panel'))

    except Exception as e:
        print(f"Error al tomar el pedido: {e}")
        flash('Ocurrió un error al tomar el pedido.')
        return redirect(url_for('repartidores.panel'))


