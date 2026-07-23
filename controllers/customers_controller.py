from models.customer import Cliente

class CustomersController:
    def __init__(self):
        self.model = Cliente()

    def listar(self):
        return self.model.obtener_clientes()

    def buscar(self, texto):
        return self.model.buscar(texto)

    def crear(self, nombre, cedula, telefono, correo, direccion):
        return self.model.crear(nombre, cedula, telefono, correo, direccion)

    def actualizar(self, id_cliente, nombre, cedula, telefono, correo, direccion):
        return self.model.actualizar(id_cliente, nombre, cedula, telefono, correo, direccion)

    def eliminar(self, id_cliente):
        return self.model.eliminar(id_cliente)