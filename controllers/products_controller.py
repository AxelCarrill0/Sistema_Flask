# controllers/products_controller.py
from flask import Blueprint, render_template, request, redirect, session, flash
from models.product import Producto
from models.categorie import Categoria

products_bp = Blueprint('productos', __name__)

@products_bp.route('/productos')
def index():
    if 'usuario' not in session:
        return redirect('/login')
    
    obj_producto = Producto()
    lista_productos = obj_producto.obtener_productos()
    
    obj_categoria = Categoria()
    categorias = obj_categoria.obtener_categorias()
    
    return render_template('products/products.html', 
                          productos=lista_productos,
                          categorias=categorias)

@products_bp.route('/productos/crear', methods=['POST'])
def crear():
    if 'usuario' not in session:
        return redirect('/login')
    
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    material = request.form['material']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    id_categoria = int(request.form['id_categoria'])
    
    obj_producto = Producto()
    obj_producto.crear(nombre, descripcion, material, precio, stock, id_categoria)
    
    flash('Producto agregado satisfactoriamente')
    return redirect('/productos')

@products_bp.route('/productos/editar/<int:id>')
def editar(id):
    if 'usuario' not in session:
        return redirect('/login')
    
    obj_producto = Producto()
    datos_producto = obj_producto.obtener_por_id(id)
    
    obj_categoria = Categoria()
    categorias = obj_categoria.obtener_categorias()
    
    return render_template('products/edit_products.html', 
                          producto=datos_producto, 
                          categorias=categorias)

@products_bp.route('/productos/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    if 'usuario' not in session:
        return redirect('/login')
    
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    material = request.form['material']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    id_categoria = int(request.form['id_categoria'])
    
    obj_producto = Producto()
    obj_producto.actualizar(id, nombre, descripcion, material, precio, stock, id_categoria)
    
    flash('Producto actualizado satisfactoriamente')
    return redirect('/productos')

@products_bp.route('/productos/eliminar/<int:id>')
def eliminar(id):
    if 'usuario' not in session:
        return redirect('/login')
    
    obj_producto = Producto()
    obj_producto.eliminar(id)
    
    flash('Producto eliminado satisfactoriamente')
    return redirect('/productos')