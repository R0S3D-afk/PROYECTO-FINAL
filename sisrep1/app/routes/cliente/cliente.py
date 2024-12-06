from flask import Blueprint, render_template
from flask_login import login_required

cliente_bp = Blueprint('cliente', __name__)

# Ruta para el dashboard del cliente
@cliente_bp.route('/dashboard')
@login_required  # Aseguramos que solo los usuarios autenticados puedan acceder
def dashboard():
    return render_template('cliente/dashboard.html')