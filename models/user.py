from config.database import mysql

class Usuario:
    
    def validar_login(self, usuario, password):
        cursor = mysql.connection.cursor()
        
        sql = """
        SELECT id_usuario, nombre, usuario 
        FROM usuarios 
        WHERE usuario = %s AND password = %s
        """
        
        cursor.execute(sql, (usuario, password))
        resultado = cursor.fetchone()
        cursor.close()
        
        return resultado 
