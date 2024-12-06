from app.db import conexion

class HistorialPedido:
    def __init__(self, id, id_pedido, id_repartidor, fecha_entrega, estado):
        self.id = id
        self.id_pedido = id_pedido
        self.id_repartidor = id_repartidor
        self.fecha_entrega = fecha_entrega
        self.estado = estado

    # Método para agregar un historial
    @staticmethod
    def create(id_pedido, id_repartidor, fecha_entrega, estado):
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO historialpedidos (id_pedido, id_repartidor, fecha_entrega, estado) VALUES (%s, %s, %s, %s)", 
                               (id_pedido, id_repartidor, fecha_entrega, estado))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"Error al crear el historial: {e}")
            return False
        finally:
            conn.close()

    # Método para obtener el historial de un pedido
    @staticmethod
    def get_by_pedido(id_pedido):
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM historialpedidos WHERE id_pedido = %s", (id_pedido,))
                historial = cursor.fetchall()
                return [HistorialPedido(**h) for h in historial]
        finally:
            conn.close()
