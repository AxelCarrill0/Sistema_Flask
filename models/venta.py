from config.database import mysql

class Venta:

    def obtener_ventas(self):
        cursor = mysql.connection.cursor()

        sql = """
        SELECT
            v.id_venta,
            v.numero_factura,
            v.fecha,
            c.nombre,
            v.total
        FROM ventas v
        INNER JOIN clientes c
            ON v.id_cliente = c.id_cliente
        ORDER BY v.id_venta DESC
        """

        cursor.execute(sql)
        resultado = cursor.fetchall()
        cursor.close()

        return resultado

    def obtener_ultima_factura(self):
        cursor = mysql.connection.cursor()

        sql = """
        SELECT numero_factura
        FROM ventas
        ORDER BY id_venta DESC
        LIMIT 1
        """

        cursor.execute(sql)

        resultado = cursor.fetchone()

        cursor.close()

        return resultado

    def crear_venta(
        self,
        numero_factura,
        subtotal,
        iva,
        total,
        id_cliente,
        id_usuario
    ):
        cursor = mysql.connection.cursor()

        sql = """
        INSERT INTO ventas
        (
            numero_factura,
            subtotal,
            iva,
            total,
            id_cliente,
            id_usuario
        )
        VALUES
        (%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(sql, (
            numero_factura,
            subtotal,
            iva,
            total,
            id_cliente,
            id_usuario
        ))

        mysql.connection.commit()

        id_venta = cursor.lastrowid

        cursor.close()

        return id_venta

    def obtener_por_id(self, id_venta):
        cursor = mysql.connection.cursor()

        sql = """
        SELECT
            v.id_venta,
            v.numero_factura,
            v.fecha,
            v.subtotal,
            v.iva,
            v.total,
            c.nombre,
            c.cedula,
            c.telefono,
            c.correo,
            c.direccion
        FROM ventas v
        INNER JOIN clientes c
            ON v.id_cliente = c.id_cliente
        WHERE v.id_venta = %s
        """

        cursor.execute(sql, (id_venta,))

        resultado = cursor.fetchone()

        cursor.close()

        return resultado