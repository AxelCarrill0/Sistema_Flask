from models.categorie import Categoria

class CategoriesController:
    def __init__(self):
        self.model = Categoria()

    def listar(self):
        return self.model.obtener_categorias()

    def crear(self, nombre, descripcion):
        return self.model.crear(nombre, descripcion)

    def actualizar(self, id_categoria, nombre, descripcion):
        return self.model.actualizar(id_categoria, nombre, descripcion)

    def eliminar(self, id_categoria):
        return self.model.eliminar(id_categoria)
