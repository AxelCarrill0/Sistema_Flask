from flask import Flask, session, redirect, render_template
from config.database import mysql, configurar_db
from controllers.auth_controller import auth_bp
from controllers.categories_controller import categories_bp
from controllers.products_controller import products_bp
from controllers.customers_controller import customers_bp
from controllers.ventas_controller import ventas_bp
from models.venta import Venta
from models.product import Producto
from models.customer import Cliente

app = Flask(__name__) 

configurar_db(app)

app.secret_key = 'sistema_flask_secret_key_123'

app.register_blueprint(auth_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(products_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(ventas_bp)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect('/login')

    obj_venta    = Venta()
    obj_producto = Producto()
    obj_cliente  = Cliente()

    total_ventas   = obj_venta.total_mes()
    total_facturas = obj_venta.contar_mes()
    total_productos = obj_producto.contar()
    total_clientes  = obj_cliente.contar()

    top_productos = obj_venta.productos_mas_vendidos(5)
    max_qty = top_productos[0][1] if top_productos else 1
    productos_mas_vendidos = [
        {
            'nombre':     p[0],
            'cantidad':   p[1],
            'porcentaje': round((p[1] / max_qty) * 100)
        }
        for p in top_productos
    ]

    alertas_raw  = obj_producto.listar_bajo_stock(5)
    alertas_stock = [
        {'nombre': p[0], 'stock': p[1]}
        for p in alertas_raw
    ]

    ultimas_raw  = obj_venta.ultimas(5)
    ultimas_ventas = [
        {
            'id_venta':       v[0],
            'numero_factura': v[1],
            'fecha':          v[2],
            'total':          v[3],
            'cliente_nombre': v[4]
        }
        for v in ultimas_raw
    ]

    return render_template('dashboard/dashboard.html',
        total_ventas           = total_ventas,
        total_facturas         = total_facturas,
        total_productos        = total_productos,
        total_clientes         = total_clientes,
        productos_mas_vendidos = productos_mas_vendidos,
        alertas_stock          = alertas_stock,
        ultimas_ventas         = ultimas_ventas
    )

if __name__ == '__main__':
    app.run(debug=True)
