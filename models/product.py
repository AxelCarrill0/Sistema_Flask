from models.base_model import BaseModel
from config.database import mysql

class Producto(BaseModel):
    def __init__(self):
        super().__init__('productos', 'id_producto')  
    
    def obtener_productos(self):
        return self.obtener_todos()

    def crear(self, nombre, descripcion, material, precio, stock, id_categoria):
        cursor = mysql.connection.cursor()
        sql = """INSERT INTO productos 
                (nombre, descripcion, material, precio, stock, id_categoria) 
                VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (nombre, descripcion, material, precio, stock, id_categoria))
        mysql.connection.commit()
        cursor.close()
    
    def actualizar(self, id_producto, nombre, descripcion, material, precio, stock, id_categoria):
        cursor = mysql.connection.cursor()
        sql = """UPDATE productos 
                SET nombre = %s, descripcion = %s, material = %s, 
                    precio = %s, stock = %s, id_categoria = %s 
                WHERE id_producto = %s"""
        cursor.execute(sql, (nombre, descripcion, material, precio, stock, id_categoria, id_producto))
        mysql.connection.commit()
        cursor.close()
    
    def eliminar(self, id_producto):
        super().eliminar(id_producto)
 
    def obtener_por_categoria(self, id_categoria):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM productos WHERE id_categoria = %s"
        cursor.execute(sql, (id_categoria,))
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    
    def actualizar_stock(self, id_producto, nuevo_stock):
        cursor = mysql.connection.cursor()
        sql = "UPDATE productos SET stock = %s WHERE id_producto = %s"
        cursor.execute(sql, (nuevo_stock, id_producto))
        mysql.connection.commit()
        cursor.close()