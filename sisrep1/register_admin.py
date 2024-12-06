from werkzeug.security import generate_password_hash
from app.db import conexion

def registrar_admin():
    nombre = 'admin'
    email = 'admin1@admin1.com'
    password = 'eladmin1234'  # Contraseña en texto plano
    rol = 'administrador'

    # Cifrar la contraseña antes de insertarla
    password_hash = generate_password_hash(password)

    conn = conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, contraseña, rol) VALUES (%s, %s, %s, %s)", 
                (nombre, email, password_hash, rol)
            )
        conn.commit()
        print("Administrador registrado exitosamente.")
    except Exception as e:
        conn.rollback()
        print(f"Error al registrar el administrador: {e}")
    finally:
        conn.close()

# Llama a esta función para registrar al administrador
registrar_admin()
