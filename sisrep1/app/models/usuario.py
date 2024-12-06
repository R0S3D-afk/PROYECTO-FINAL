from werkzeug.security import generate_password_hash, check_password_hash
from app.db import conexion
from flask_login import UserMixin  # Importamos UserMixin para integrarlo con Flask-Login

class Usuario(UserMixin):  # Heredamos de UserMixin para usar las funcionalidades de Flask-Login
    def __init__(self, id, nombre, email, rol):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.rol = rol

    # Método para obtener un usuario por su ID
    @staticmethod
    def get_by_id(id):
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
                user_data = cursor.fetchone()
                if user_data:
                    return Usuario(id=user_data['id'], nombre=user_data['nombre'], email=user_data['email'], rol=user_data['rol'])
                return None
        finally:
            conn.close()

    # Método para obtener un usuario por su email
    @staticmethod
    def get_by_email(email):
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
                user_data = cursor.fetchone()
                if user_data:
                    return Usuario(id=user_data['id'], nombre=user_data['nombre'], email=user_data['email'], rol=user_data['rol'])
                return None
        finally:
            conn.close()

    # Método para crear un nuevo usuario
    @staticmethod
    def create(nombre, email, password, rol):
        conn = conexion()
        try:
            password_hash = generate_password_hash(password)  # Cifrar la contraseña

            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuarios (nombre, email, contraseña, rol) VALUES (%s, %s, %s, %s)", 
                    (nombre, email, password_hash, rol)
                )
                conn.commit()

            return True
        except Exception as e:
            conn.rollback()
            print(f"Error al crear el usuario: {e}")
            return False
        finally:
            conn.close()

    # Método para verificar la contraseña del usuario
    def check_password(self, password):
        return check_password_hash(self.password, password)

