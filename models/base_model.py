from config.database import mysql
from abc import ABC, abstractmethod

class BaseModel(ABC):
    def __init__(self, nombre_tabla, clave_primaria):
        self.nombre_tabla = nombre_tabla
        self.clave_primaria = clave_primaria
    
    def obtener_todos(self):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM {self.nombre_tabla}"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    
    def obtener_por_id(self, id_valor):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM {self.nombre_tabla} WHERE {self.clave_primaria} = %s"
        cursor.execute(sql, (id_valor,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado
    
    def eliminar(self, id_valor):
        cursor = mysql.connection.cursor()
        sql = f"DELETE FROM {self.nombre_tabla} WHERE {self.clave_primaria} = %s"
        cursor.execute(sql, (id_valor,))
        mysql.connection.commit()
        cursor.close()
    
    @abstractmethod
    def crear(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def actualizar(self, *args, **kwargs):
        pass