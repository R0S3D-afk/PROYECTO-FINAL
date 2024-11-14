
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import conexion

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE email = %s AND contraseña = %s", (email, password))
                user = cursor.fetchone()
                if user:
                    flash('Inicio de sesión exitoso', 'success')
                    return redirect(url_for('pedidos.mostrar_pedidos'))
                else:
                    flash('Email o contraseña incorrecta', 'danger')
        finally:
            conn.close()

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        rol = 'cliente'  # se puede cambiar dependiendo del usuario 
        conn = conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO usuarios (nombre, email, contraseña, rol) VALUES (%s, %s, %s, %s)", 
                               (nombre, email, password, rol))
            conn.commit()
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        finally:
            conn.close()

    return render_template('auth/register.html')

