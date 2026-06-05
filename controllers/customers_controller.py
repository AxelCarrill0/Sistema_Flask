from flask import Blueprint, render_template, request, redirect, session
from models.customer import Cliente

customers_bp = Blueprint('clientes', __name__)

#Listar Clientes
@customers_bp.route('/clientes')
def listarclientes():

    if 'usuario' not in session:
        return redirect('/login')

    obj_cliente = Cliente()

    texto_busqueda = request.args.get('buscar')

    if texto_busqueda:
        clientes = obj_cliente.buscar(texto_busqueda)
    else:
        clientes = obj_cliente.obtener_clientes()

    return render_template(
        'customers/customers.html',
        clientes=clientes
    )

#Crear
@customers_bp.route('/clientes/crear', methods=['POST'])
def crear():

    if 'usuario' not in session:
        return redirect('/login')

    nombre = request.form['nombre']
    cedula = request.form['cedula']
    telefono = request.form['telefono']
    correo = request.form['correo']
    direccion = request.form['direccion']

    obj_cliente = Cliente()

    obj_cliente.crear(
        nombre,
        cedula,
        telefono,
        correo,
        direccion
    )

    return redirect('/clientes')

#Editar 
@customers_bp.route('/clientes/editar/<int:id>')
def editar(id):

    if 'usuario' not in session:
        return redirect('/login')

    obj_cliente = Cliente()

    cliente = obj_cliente.obtener_por_id(id)

    return render_template(
        'customers/edit_customer.html',
        cliente=cliente
    )

#Actualizar
@customers_bp.route('/clientes/actualizar/<int:id>', methods=['POST'])
def actualizar(id):

    if 'usuario' not in session:
        return redirect('/login')

    nombre = request.form['nombre']
    cedula = request.form['cedula']
    telefono = request.form['telefono']
    correo = request.form['correo']
    direccion = request.form['direccion']

    obj_cliente = Cliente()

    obj_cliente.actualizar(
        id,
        nombre,
        cedula,
        telefono,
        correo,
        direccion
    )

    return redirect('/clientes')

#Eliminar
@customers_bp.route('/clientes/eliminar/<int:id>')
def eliminar(id):

    if 'usuario' not in session:
        return redirect('/login')

    obj_cliente = Cliente()

    obj_cliente.eliminar(id)

    return redirect('/clientes')