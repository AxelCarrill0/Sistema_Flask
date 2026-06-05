from flask import Blueprint, render_template, request, redirect, session
from models.user import Usuario

# Definimos el Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def validar_login():
    if 'usuario' in session:
        return redirect('/dashboard')

    if request.method == 'POST':
        txt_usuario = request.form['usuario']
        txt_password = request.form['password']

        # Usamos la POO para validar los datos
        obj_usuario = Usuario()
        datos_usuario = obj_usuario.validar_login(txt_usuario, txt_password)

        if datos_usuario:
            session['usuario'] = datos_usuario[1]  
            return redirect('/dashboard')
        else:
            return render_template('auth/login.html', error_msg="Usuario o contraseña incorrectos")

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
