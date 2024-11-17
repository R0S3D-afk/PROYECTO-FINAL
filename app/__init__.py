from flask import Flask
from app.routes.auth.login import auth_bp
from app.routes.pedidos.pedidos import pedidos_bp
from app.routes.repartidores.ver_calificaciones import calificaciones_bp
from app.routes.historial.historial import historial_bp
from app.routes.repartidores.repartidores import repartidores_bp
from app.routes.pedidos.crear_pedido import crear_pedido_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'LOok2039340409'

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    app.register_blueprint(crear_pedido_bp)
    app.register_blueprint(calificaciones_bp, url_prefix='/repartidores/calificaciones')  # Cambiado para incluir el prefijo correcto
    app.register_blueprint(repartidores_bp, url_prefix='/repartidores/repartidores')  # Cambiado para incluir el prefijo correcto
    app.register_blueprint(historial_bp, url_prefix='/historial')

    return app