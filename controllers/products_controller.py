from models.product import Producto

class ProductsController:
    def __init__(self):
        self.model = Producto()

    def listar(self):
        return self.model.obtener_productos()

    def obtener_por_id(self, id_producto):
        return self.model.obtener_por_id(id_producto)

    def crear(self, nombre, descripcion, material, precio, stock, id_categoria):
        return self.model.crear(nombre, descripcion, material, precio, stock, id_categoria)

    def actualizar(self, id_producto, nombre, descripcion, material, precio, stock, id_categoria):
        return self.model.actualizar(id_producto, nombre, descripcion, material, precio, stock, id_categoria)

    def eliminar(self, id_producto):
        return self.model.eliminar(id_producto)