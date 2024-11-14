from flask import Blueprint, render_template

repartidores_bp = Blueprint('repartidores', __name__)

@repartidores_bp.route('/')
def ver_repartidores():
    return render_template('repartidores/calificaciones.html')
