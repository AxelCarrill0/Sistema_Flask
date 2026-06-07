from config.database import mysql

class DetalleVenta:

    def crear_detalle(
        self,
        id_venta,
        id_producto,
        cantidad,
        precio_unitario,
        subtotal
    ):
        cursor = mysql.connection.cursor()

        sql = """
        INSERT INTO detalle_ventas
        (
            id_venta,
            id_producto,
            cantidad,
            precio_unitario,
            subtotal
        )
        VALUES
        (%s,%s,%s,%s,%s)
        """

        cursor.execute(sql, (
            id_venta,
            id_producto,
            cantidad,
            precio_unitario,
            subtotal
        ))

        mysql.connection.commit()

        cursor.close()

    def obtener_detalles(self, id_venta):
        cursor = mysql.connection.cursor()

        sql = """
        SELECT
            p.nombre,
            d.cantidad,
            d.precio_unitario,
            d.subtotal
        FROM detalle_ventas d
        INNER JOIN productos p
            ON d.id_producto = p.id_producto
        WHERE d.id_venta = %s
        """

        cursor.execute(sql, (id_venta,))

        resultado = cursor.fetchall()

        cursor.close()

        return resultado