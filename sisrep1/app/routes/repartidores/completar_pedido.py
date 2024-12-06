from flask import Blueprint, redirect, url_for
from app.models.pedido import Pedido

completar_pedido = Blueprint('repartidores', __name__)

@completar_pedido.route('/completar_pedido/<int:pedido_id>')
def completar(pedido_id):
    if Pedido.marcar_como_entregado(pedido_id):
        return redirect(url_for('repartidores.dashboard'))

    return "Error al completar el pedido", 500
