from app.db import conexion

class Repartidor:
    def __init__(self, id, id_usuario, tipo_transporte, licencia=None):
        self.id = id
        self.id_usuario = id_usuario
        self.tipo_transporte = tipo_transporte
        self.licencia = licencia

    # Método para crear un repartidor
    @staticmethod
    def create(id_usuario, tipo_transporte, licencia=None):
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO repartidores (id_usuario, tipo_transporte, licencia) VALUES (%s, %s, %s)",
                    (id_usuario, tipo_transporte, licencia)
                )
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"Error al crear el repartidor: {e}")
            return False
        finally:
            conn.close()


    # Método para obtener un repartidor por ID
    @staticmethod
    def get_by_id(id):
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM repartidores WHERE id = %s", (id,))
                repartidor_data = cursor.fetchone()
                if repartidor_data:
                    return Repartidor(**repartidor_data)
                return None
        finally:
            conn.close()

    # Método para obtener un repartidor por ID de usuario
    @staticmethod
    def get_by_usuario_id(usuario_id):
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM repartidores WHERE id_usuario = %s", (usuario_id,)
                )
                repartidor_data = cursor.fetchone()
                if repartidor_data:
                    return Repartidor(**repartidor_data)
                return None
        finally:
            conn.close()

    # Método para actualizar el perfil de un repartidor
    def update(self):
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE repartidores SET tipo_transporte = %s, licencia = %s WHERE id = %s",
                    (self.tipo_transporte, self.licencia, self.id)
                )
                conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error al actualizar el repartidor: {e}")
        finally:
            conn.close()
