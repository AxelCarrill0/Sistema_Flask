from flask import Blueprint, render_template, request, redirect, session, flash

from models.customer import Cliente
from models.product import Producto
from models.venta import Venta
from models.detalle_venta import DetalleVenta

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/ventas')
def index():

    if 'usuario' not in session:
        return redirect('/login')

    obj_cliente = Cliente()
    clientes = obj_cliente.obtener_clientes()

    obj_producto = Producto()
    productos = obj_producto.obtener_productos()

    obj_venta = Venta()
    ventas = obj_venta.obtener_ventas()

    if 'carrito' not in session:
        session['carrito'] = []

    carrito = session['carrito']

    subtotal = sum(item['subtotal'] for item in carrito)

    iva = round(subtotal * 0.15, 2)

    total = subtotal + iva

    cliente_seleccionado = session.get('id_cliente')

    return render_template(
        'ventas/ventas.html',
        clientes=clientes,
        productos=productos,
        carrito=carrito,
        ventas=ventas,
        subtotal=subtotal,
        iva=iva,
        total=total,
        cliente_seleccionado=cliente_seleccionado
    )

@ventas_bp.route('/ventas/agregar_producto', methods=['POST'])
def agregar_producto():

    if 'usuario' not in session:
        return redirect('/login')

    id_cliente = int(request.form['id_cliente'])
    session['id_cliente'] = id_cliente

    id_producto = int(request.form['id_producto'])
    cantidad = int(request.form['cantidad'])

    obj_producto = Producto()
    producto = obj_producto.obtener_por_id(id_producto)

    if not producto:
        flash('Producto no encontrado')
        return redirect('/ventas')

    stock_actual = producto[5]
    precio = float(producto[4])

    carrito = session.get('carrito', [])

    producto_existe = False

    for item in carrito:

        if item['id_producto'] == id_producto:

            nueva_cantidad = item['cantidad'] + cantidad

            if nueva_cantidad > stock_actual:
                flash(f'Stock insuficiente. Disponible: {stock_actual}')
                return redirect('/ventas')

            item['cantidad'] = nueva_cantidad
            item['subtotal'] = nueva_cantidad * item['precio']

            producto_existe = True
            break

    if not producto_existe:

        if cantidad > stock_actual:
            flash(f'Stock insuficiente. Disponible: {stock_actual}')
            return redirect('/ventas')

        nuevo_item = {
            'id_producto': producto[0],
            'nombre': producto[1],
            'cantidad': cantidad,
            'precio': precio,
            'subtotal': precio * cantidad
        }

        carrito.append(nuevo_item)

    session['carrito'] = carrito

    flash('Producto agregado al carrito')
    return redirect('/ventas')

@ventas_bp.route('/ventas/eliminar_producto/<int:index>')
def eliminar_producto(index):

    if 'usuario' not in session:
        return redirect('/login')

    carrito = session.get('carrito', [])

    if 0 <= index < len(carrito):
        carrito.pop(index)

    session['carrito'] = carrito

    return redirect('/ventas')

@ventas_bp.route('/ventas/registrar', methods=['POST'])
def registrar():

    if 'usuario' not in session:
        return redirect('/login')

    carrito = session.get('carrito', [])

    if len(carrito) == 0:
        return redirect('/ventas')

    id_cliente = session.get('id_cliente')

    subtotal = sum(item['subtotal'] for item in carrito)

    iva = round(subtotal * 0.15, 2)

    total = subtotal + iva

    obj_venta = Venta()

    ultima_factura = obj_venta.obtener_ultima_factura()

    if ultima_factura:
        ultimo_numero = int(
            ultima_factura[0].replace('FAC-', '')
        )

        numero_factura = f"FAC-{ultimo_numero + 1:06d}"

    else:
        numero_factura = "FAC-000001"

    id_usuario = session['id_usuario']

    id_venta = obj_venta.crear_venta(
        numero_factura,
        subtotal,
        iva,
        total,
        id_cliente,
        id_usuario
    )

    obj_detalle = DetalleVenta()

    obj_producto = Producto()

    for item in carrito:

        obj_detalle.crear_detalle(
            id_venta,
            item['id_producto'],
            item['cantidad'],
            item['precio'],
            item['subtotal']
        )

        producto = obj_producto.obtener_por_id(
            item['id_producto']
        )

        nuevo_stock = producto[5] - item['cantidad']

        obj_producto.actualizar_stock(
            item['id_producto'],
            nuevo_stock
        )

    session['carrito'] = []

    session.pop('id_cliente', None)

    return redirect('/ventas')

@ventas_bp.route('/ventas/detalle/<int:id_venta>')
def detalle(id_venta):

    if 'usuario' not in session:
        return redirect('/login')

    obj_venta = Venta()
    venta = obj_venta.obtener_por_id(id_venta)

    obj_detalle = DetalleVenta()
    detalles = obj_detalle.obtener_detalles(id_venta)

    return render_template(
        'ventas/detalle_venta.html',
        venta=venta,
        detalles=detalles
    )

@ventas_bp.route('/ventas/factura/<int:id_venta>')
def factura(id_venta):

    if 'usuario' not in session:
        return redirect('/login')

    obj_venta = Venta()
    venta = obj_venta.obtener_por_id(id_venta)

    obj_detalle = DetalleVenta()
    detalles = obj_detalle.obtener_detalles(id_venta)

    return render_template(
        'ventas/factura.html',
        venta=venta,
        detalles=detalles
    )