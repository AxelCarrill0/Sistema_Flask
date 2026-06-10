from flask import Flask, redirect
from config.database import configurar_db
from controllers.auth_controller import auth_bp
from controllers.categories_controller import categories_bp
from controllers.products_controller import products_bp
from controllers.customers_controller import customers_bp
from controllers.sales_controller import ventas_bp
from controllers.dashboard_controller import dashboard_bp

app = Flask(__name__) 

configurar_db(app)

app.secret_key = 'sistema_flask_secret_key_123'

app.register_blueprint(auth_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(products_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def index():
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
