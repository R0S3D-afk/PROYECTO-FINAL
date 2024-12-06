from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import conexion
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models.usuario import Usuario

# Crear el blueprint para la autenticación
auth_bp = Blueprint('auth', __name__)

# Ruta para iniciar sesión
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Establecer conexión a la base de datos
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
                user = cursor.fetchone()
                
                if user and check_password_hash(user['contraseña'], password):
                    # Verificar que la contraseña coincida con la almacenada
                    # Crear el usuario en Flask-Login
                    usuario = Usuario(id=user['id'], nombre=user['nombre'], email=user['email'], rol=user['rol'])
                    login_user(usuario)  # Iniciar sesión con Flask-Login
                    
                    flash('Inicio de sesión exitoso', 'success')
                    
                    # Redirigir dependiendo del rol del usuario
                    if usuario.rol == 'administrador':
                        return redirect(url_for('admin.dashboard'))  # Panel del admin
                    elif usuario.rol == 'repartidor':
                        return redirect(url_for('repartidores.panel'))  # Panel del repartidor
                    else:
                        return redirect(url_for('pedidos.mostrar_pedidos'))  # Página de pedidos para clientes
                else:
                    flash('Email o contraseña incorrecta', 'danger')
        finally:
            conn.close()

    return render_template('auth/login.html')

# Ruta para el registro de usuario
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']  # Asumiendo que se selecciona entre 'cliente' o 'repartidor'
        
        # Validar que los campos no estén vacíos
        if not nombre or not email or not password or not rol:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('auth.register'))

        # Verificar si el email ya está registrado
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
                existing_user = cursor.fetchone()
                if existing_user:
                    flash('El correo electrónico ya está registrado.', 'danger')
                    return redirect(url_for('auth.register'))
                
                # Hash de la contraseña
                hashed_password = generate_password_hash(password)
                
                # Insertar el nuevo usuario en la base de datos
                cursor.execute("INSERT INTO usuarios (nombre, email, contraseña, rol) VALUES (%s, %s, %s, %s)",
                               (nombre, email, hashed_password, rol))
                conn.commit()
                flash('Usuario registrado exitosamente.', 'success')
                
                # Redirigir al login después del registro
                return redirect(url_for('auth.login'))
        finally:
            conn.close()

    return render_template('auth/register.html')


# Ruta para cerrar sesión
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()  # Esto cierra la sesión del usuario
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('auth.login'))  # Redirige a la página de login
