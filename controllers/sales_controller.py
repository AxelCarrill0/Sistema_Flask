from models.sale import Venta
from models.sale_detail import DetalleVenta
from models.product import Producto

class SalesController:
    def __init__(self):
        self.sale_model = Venta()
        self.detail_model = DetalleVenta()
        self.product_model = Producto()

    def obtener_ventas(self):
        return self.sale_model.obtener_ventas()

    def obtener_venta_por_id(self, id_venta):
        return self.sale_model.obtener_por_id(id_venta)

    def obtener_detalles_venta(self, id_venta):
        return self.detail_model.obtener_detalles(id_venta)

    def procesar_venta(self, id_cliente, id_usuario, carrito):
        subtotal = sum(item['subtotal'] for item in carrito)
        iva = round(subtotal * 0.15, 2)
        total = subtotal + iva

        ultima = self.sale_model.obtener_ultima_factura()
        if ultima and ultima[0]:
            try:
                ultimo_num = int(ultima[0].replace("FAC-", ""))
                numero_factura = f"FAC-{ultimo_num + 1:06d}"
            except ValueError:
                numero_factura = "FAC-000001"
        else:
            numero_factura = "FAC-000001"

        id_venta = self.sale_model.crear_venta(
            numero_factura, subtotal, iva, total, id_cliente, id_usuario
        )

        for item in carrito:
            self.detail_model.crear_detalle(
                id_venta, item['id_producto'], item['cantidad'], item['precio'], item['subtotal']
            )
            prod = self.product_model.obtener_por_id(item['id_producto'])
            if prod:
                nuevo_stock = prod[5] - item['cantidad']
                self.product_model.actualizar_stock(item['id_producto'], nuevo_stock)

        return id_venta, numero_factura