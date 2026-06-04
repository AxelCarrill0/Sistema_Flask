from flask import Flask, render_template, request, redirect

from config.database import configurar_db
from models.usuarios import Usuario

app = Flask(__name__)

configurar_db(app)


@app.route('/')
def login():
    return render_template('login/login.html')


@app.route('/validar_login', methods=['POST'])
def validar_login():

    usuario = request.form['usuario']
    password = request.form['password']

    usuario_model = Usuario()

    if usuario_model.validar_login(usuario, password):
        return redirect('/dashboard')

    return "Usuario o contraseña incorrectos"


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)