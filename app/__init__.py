from flask import Flask
from app.routes.auth.login import auth_bp
from app.routes.pedidos.pedidos import pedidos_bp
from app.routes.repartidores.ver_calificaciones import calificaciones_bp
from app.routes.historial.historial import historial_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'LOok2039340409'

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    app.register_blueprint(calificaciones_bp, url_prefix='/repartidores')
    app.register_blueprint(historial_bp, url_prefix='/historial')

    return app
