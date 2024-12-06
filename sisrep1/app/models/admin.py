from flask_login import UserMixin
from app.db import conexion

class Usuario(UserMixin):
    def __init__(self, id, nombre, email, rol):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.rol = rol

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
