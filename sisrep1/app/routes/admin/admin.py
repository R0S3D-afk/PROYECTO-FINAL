from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from app.db import conexion

admin_bp = Blueprint('admin', __name__)

# Ruta para el dashboard del administrador
@admin_bp.route('/dashboard')
@login_required  # Solo accesible si el usuario está autenticado
def dashboard():
    return render_template('admin/dashboard.html')

# Ruta para ver los usuarios
@admin_bp.route('/usuarios')
@login_required
def ver_usuarios():
    conn = conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()  # Obtener todos los usuarios
        return render_template('admin/ver_usuarios.html', usuarios=usuarios)
    except Exception as e:
        flash(f'Error al obtener los usuarios: {e}', 'danger')
        return redirect(url_for('admin.dashboard'))
    finally:
        conn.close()

# Ruta para ver los pedidos pendientes y en tránsito
@admin_bp.route('/pedidos')
@login_required
def ver_pedidos():
    conn = conexion()
    try:
        with conn.cursor() as cursor:
            # Pedidos pendientes
            cursor.execute("SELECT * FROM pedidos WHERE estado = 'pendiente'")
            pedidos_pendientes = cursor.fetchall()

            # Pedidos en tránsito
            cursor.execute("SELECT * FROM pedidos WHERE estado = 'en_transito'")
            pedidos_en_transito = cursor.fetchall()

        return render_template('admin/ver_pedidos.html',
                               pedidos_pendientes=pedidos_pendientes,
                               pedidos_en_transito=pedidos_en_transito)
    except Exception as e:
        flash(f'Error al obtener los pedidos: {e}', 'danger')
        return redirect(url_for('admin.dashboard'))
    finally:
        conn.close()

# Ruta para ver el historial de los envíos (con repartidor y cliente)
@admin_bp.route('/historial')
@login_required
def ver_historial():
    conn = conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT h.id, h.fecha_entrega, h.estado, p.id_cliente, r.id_usuario AS repartidor_id
                FROM historialpedidos h
                JOIN pedidos p ON h.id_pedido = p.id
                LEFT JOIN repartidores r ON h.id_repartidor = r.id
            """)
            historial = cursor.fetchall()

            # Obtener información adicional sobre los clientes y repartidores
            for item in historial:
                cursor.execute("SELECT nombre FROM usuarios WHERE id = %s", (item['id_cliente'],))
                item['cliente_nombre'] = cursor.fetchone()['nombre']
                if item['repartidor_id']:
                    cursor.execute("SELECT nombre FROM usuarios WHERE id = %s", (item['repartidor_id'],))
                    item['repartidor_nombre'] = cursor.fetchone()['nombre']
                else:
                    item['repartidor_nombre'] = "No asignado"

        return render_template('admin/ver_historial.html', historial=historial)
    except Exception as e:
        flash(f'Error al obtener el historial: {e}', 'danger')
        return redirect(url_for('admin.dashboard'))
    finally:
        conn.close()

# Ruta para ver los repartidores
@admin_bp.route('/repartidores')
@login_required
def ver_repartidores():
    conn = conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM repartidores")
            repartidores = cursor.fetchall()
        return render_template('admin/ver_repartidores.html', repartidores=repartidores)
    except Exception as e:
        flash(f'Error al obtener los repartidores: {e}', 'danger')
        return redirect(url_for('admin.dashboard'))
    finally:
        conn.close()

# Ruta para eliminar un repartidor
@admin_bp.route('/repartidores/eliminar/<int:id_repartidor>', methods=['GET', 'POST'])
@login_required
def eliminar_repartidor(id_repartidor):
    try:
        conn = conexion()
        with conn.cursor() as cursor:
            # Eliminar repartidor de la base de datos
            cursor.execute("DELETE FROM repartidores WHERE id = %s", (id_repartidor,))
            conn.commit()
            flash(f'Repartidor con ID {id_repartidor} eliminado exitosamente.', 'success')
            return redirect(url_for('admin.ver_repartidores'))
    except Exception as e:
        flash(f'Error al eliminar el repartidor: {e}', 'danger')
        return redirect(url_for('admin.ver_repartidores'))
    finally:
        conn.close()
