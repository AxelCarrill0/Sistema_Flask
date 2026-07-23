from models.sale import Venta
from models.product import Producto
from models.customer import Cliente

class DashboardController:
    def __init__(self):
        self.sale_model = Venta()
        self.product_model = Producto()
        self.customer_model = Cliente()

    def obtener_metricas(self):
        total_ventas = self.sale_model.total_mes()
        total_facturas = self.sale_model.contar_mes()
        total_productos = self.product_model.contar()
        total_clientes = self.customer_model.contar()

        top_productos = self.sale_model.productos_mas_vendidos(5)
        alertas_stock = self.product_model.listar_bajo_stock(5)
        ultimas_ventas = self.sale_model.ultimas(5)

        return {
            'total_ventas': total_ventas,
            'total_facturas': total_facturas,
            'total_productos': total_productos,
            'total_clientes': total_clientes,
            'top_productos': top_productos,
            'alertas_stock': alertas_stock,
            'ultimas_ventas': ultimas_ventas
        }
