from app.db import conexion

class Pedido:
    def __init__(self, id, id_cliente, direccion_entrega, contenido, urgencia, estado, fecha_pedido, id_repartidor=None):
        self.id = id
        self.id_cliente = id_cliente
        self.direccion_entrega = direccion_entrega
        self.contenido = contenido
        self.urgencia = urgencia
        self.estado = estado
        self.fecha_pedido = fecha_pedido
        self.id_repartidor = id_repartidor

    # Método para crear un pedido
    @staticmethod
    def create(id_cliente, direccion_entrega, contenido, urgencia, estado='pendiente', id_repartidor=None):
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pedidos (id_cliente, direccion_entrega, contenido, urgencia, estado, id_repartidor) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (id_cliente, direccion_entrega, contenido, urgencia, estado, id_repartidor))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"Error al crear el pedido: {e}")
            return False
        finally:
            conn.close()

    # Método para obtener todos los pedidos
    @staticmethod
    def get_all():
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM pedidos WHERE estado = 'pendiente' OR estado = 'en_transito'")
                pedidos = cursor.fetchall()
                return [Pedido(**pedido) for pedido in pedidos]
        finally:
            conn.close()

    # Método para obtener pedidos por estado (pendiente, en tránsito, completado)
    @staticmethod
    def get_by_estado(estado):
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM pedidos WHERE estado = %s", (estado,))
                pedidos = cursor.fetchall()
                return [Pedido(**pedido) for pedido in pedidos]
        finally:
            conn.close()

    # Método para obtener un pedido por su ID
    @staticmethod
    def get_by_id(id):
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM pedidos WHERE id = %s", (id,))
                pedido_data = cursor.fetchone()
                if pedido_data:
                    return Pedido(**pedido_data)
                return None
        finally:
            conn.close()

    # Método para asignar un pedido a un repartidor
    @staticmethod
    def asignar_a_repartidor(pedido_id, repartidor_id):
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                # Actualizar el pedido para asignarle al repartidor
                cursor.execute("UPDATE pedidos SET id_repartidor = %s, estado = 'en_transito' WHERE id = %s AND estado = 'pendiente'", (repartidor_id, pedido_id))
                conn.commit()
                if cursor.rowcount > 0:
                    return True
                return False
        except Exception as e:
            conn.rollback()
            print(f"Error al actualizar el pedido: {e}")
            return False
        finally:
            conn.close()
            
            
    # Método para cambiar el estado de un pedido
    @staticmethod
    def update(id, estado, id_repartidor):
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE pedidos 
                    SET estado = %s, id_repartidor = %s
                    WHERE id = %s
                """, (estado, id_repartidor, id))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"Error al actualizar el pedido: {e}")
            return False
        finally:
            conn.close()

    # Método para obtener los pedidos atendidos (completados)
    @staticmethod
    def get_completados():
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM pedidos WHERE estado = 'completado'")
                pedidos = cursor.fetchall()
                return [Pedido(**pedido) for pedido in pedidos]
        finally:
            conn.close()
