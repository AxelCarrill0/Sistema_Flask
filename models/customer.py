from models.base_model import BaseModel
from config.database import mysql

class Cliente(BaseModel):

    def __init__(self):
        super().__init__('clientes', 'id_cliente')

    def obtener_clientes(self):
        return self.obtener_todos()

    def crear(self, nombre, cedula, telefono, correo, direccion):
        cursor = mysql.connection.cursor()

        sql = """
        INSERT INTO clientes
        (nombre, cedula, telefono, correo, direccion)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            nombre,
            cedula,
            telefono,
            correo,
            direccion
        ))

        mysql.connection.commit()
        cursor.close()

    def actualizar(self, id_cliente, nombre, cedula, telefono, correo, direccion):
        cursor = mysql.connection.cursor()

        sql = """
        UPDATE clientes
        SET nombre=%s,
            cedula=%s,
            telefono=%s,
            correo=%s,
            direccion=%s
        WHERE id_cliente=%s
        """

        cursor.execute((
            sql
        ), (
            nombre,
            cedula,
            telefono,
            correo,
            direccion,
            id_cliente
        ))

        mysql.connection.commit()
        cursor.close()

    def eliminar(self, id_cliente):
        super().eliminar(id_cliente)

    def buscar(self, texto):
        cursor = mysql.connection.cursor()

        sql = """
        SELECT *
        FROM clientes
        WHERE nombre LIKE %s
        OR cedula LIKE %s
        """

        criterio = f"%{texto}%"

        cursor.execute(sql, (criterio, criterio))

        resultado = cursor.fetchall()

        cursor.close()

        return resultado