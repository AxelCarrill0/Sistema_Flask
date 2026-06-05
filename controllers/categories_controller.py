from flask import Blueprint, render_template, request, redirect, session
from models.categorie import Categoria

categories_bp = Blueprint('categorias', __name__)

@categories_bp.route('/categorias')
def index():
    if 'usuario' not in session:
        return redirect('/login')
    
    obj_categoria = Categoria()
    lista_categorias = obj_categoria.obtener_categorias()
    
    # Renderizamos la vista principal de categorías pasándole la lista
    return render_template('products/categories.html', categorias=lista_categorias)

# 2. Ruta para CREAR una nueva categoría (Petición POST)
@categories_bp.route('/categorias/crear', methods=['POST'])
def crear():
    if 'usuario' not in session:
        return redirect('/login')
        
    txt_nombre = request.form['nombre']
    txt_descripcion = request.form['descripcion']
    
    obj_categoria = Categoria()
    obj_categoria.crear(txt_nombre, txt_descripcion)
    
    return redirect('/categorias')

# 3. Ruta para MOSTRAR el formulario de edición (Petición GET)
@categories_bp.route('/categorias/editar/<int:id>')
def editar(id):
    if 'usuario' not in session:
        return redirect('/login')
        
    obj_categoria = Categoria()
    datos_categoria = obj_categoria.obtener_por_id(id)
    
    # Renderizamos la plantilla para editar pasándole los datos de esa categoría
    return render_template('products/edit_categories.html', categoria=datos_categoria)

# 4. Ruta para PROCESAR la edición (Petición POST)
@categories_bp.route('/categorias/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    if 'usuario' not in session:
        return redirect('/login')
        
    txt_nombre = request.form['nombre']
    txt_descripcion = request.form['descripcion']
    
    obj_categoria = Categoria()
    obj_categoria.actualizar(id, txt_nombre, txt_descripcion)
    
    return redirect('/categorias')

# 5. Ruta para ELIMINAR una categoría (Petición GET, simple como el tutorial)
@categories_bp.route('/categorias/eliminar/<int:id>')
def eliminar(id):
    if 'usuario' not in session:
        return redirect('/login')
        
    obj_categoria = Categoria()
    obj_categoria.eliminar(id)
    
    return redirect('/categorias')
