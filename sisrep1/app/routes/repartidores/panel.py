from flask import Blueprint, render_template
from app.models.pedido import Pedido
from app.models.repartidor import Repartidor

panel = Blueprint('repartidores', __name__)

@panel.route('/panel')
def dashboard():
    # Aquí obtenemos los pedidos pendientes
    pedidos_pendientes = Pedido.get_pedidos_pendientes()
    return render_template('repartidores/dashboard.html', pedidos=pedidos_pendientes)
