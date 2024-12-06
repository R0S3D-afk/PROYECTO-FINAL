from flask import Flask
from flask_login import LoginManager

# Importar los blueprints de las rutas
from app.routes.auth.login import auth_bp
from app.routes.pedidos.pedidos import pedidos_bp
from app.routes.pedidos.crear_pedido import crear_pedido_bp
from app.routes.repartidores.repartidores import repartidores_bp
from app.routes.repartidores.ver_calificaciones import calificaciones_bp
from app.routes.historial.historial import historial_bp
from app.routes.admin.admin import admin_bp  # Blueprint del admin
from app.models.usuario import Usuario  # Modelo del usuario para el user_loader

def create_app():
    # Crear la instancia de la aplicación Flask
    app = Flask(__name__)
    app.config['DEBUG'] = True

    # Configuración de la clave secreta para sesiones y formularios
    app.config['SECRET_KEY'] = 'LOok2039340409'  # Asegúrate de cambiar esto por una clave secreta más segura en producción

    # Configuración de Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirigir a la ruta de login si el usuario no está autenticado

    # Cargar el usuario de la base de datos usando su ID (requerido por Flask-Login)
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.get_by_id(user_id)

    # Registro de blueprints con sus respectivas URLs
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Rutas de autenticación
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')  # Rutas para ver los pedidos
    app.register_blueprint(crear_pedido_bp, url_prefix='/pedidos')  # Ruta para crear pedidos
    app.register_blueprint(repartidores_bp, url_prefix='/repartidores')  # Rutas de repartidores
    app.register_blueprint(calificaciones_bp, url_prefix='/repartidores/calificaciones')  # Rutas de calificaciones de repartidores
    app.register_blueprint(historial_bp, url_prefix='/historial')  # Rutas de historial
    app.register_blueprint(admin_bp, url_prefix='/admin')  # Rutas de administración

    return app
