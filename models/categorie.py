from models.base_model import BaseModel
from config.database import mysql

class Categoria(BaseModel):
    def __init__(self):
        super().__init__('categorias', 'id_categoria')
    
    def obtener_categorias(self):
        return self.obtener_todos()
    
    def crear(self, nombre, descripcion):
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)"
        cursor.execute(sql, (nombre, descripcion))
        mysql.connection.commit()
        cursor.close()
    
    def actualizar(self, id_categoria, nombre, descripcion):
        cursor = mysql.connection.cursor()
        sql = "UPDATE categorias SET nombre = %s, descripcion = %s WHERE id_categoria = %s"
        cursor.execute(sql, (nombre, descripcion, id_categoria))
        mysql.connection.commit()
        cursor.close()
    
    def eliminar(self, id_categoria):
        super().eliminar(id_categoria)