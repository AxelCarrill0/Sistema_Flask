from flask import Flask, session, redirect, render_template
from config.database import mysql, configurar_db
from controllers.auth import auth_bp

app = Flask(__name__)

configurar_db(app)

app.secret_key = 'sistema_flask_secret_key_123'

app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect('/login')
    return render_template('dashboard/dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
