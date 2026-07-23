from config.database import mysql

class Usuario:
    def asegurar_columna_rostro(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'usuarios'
              AND COLUMN_NAME = 'rostro_activo'
            """
        )
        existe = cursor.fetchone()[0] > 0

        if not existe:
            cursor.execute(
                "ALTER TABLE usuarios ADD COLUMN rostro_activo TINYINT(1) NOT NULL DEFAULT 0"
            )
            mysql.connection.commit()

        cursor.close()

    def obtener_por_id(self, id_usuario):
        self.asegurar_columna_rostro()
        cursor = mysql.connection.cursor()

        sql = """
        SELECT id_usuario, nombre, usuario, rostro_activo
        FROM usuarios
        WHERE id_usuario = %s
        """

        cursor.execute(sql, (id_usuario,))
        resultado = cursor.fetchone()
        cursor.close()

        return resultado

    def activar_rostro(self, id_usuario):
        self.asegurar_columna_rostro()
        cursor = mysql.connection.cursor()

        sql = "UPDATE usuarios SET rostro_activo = 1 WHERE id_usuario = %s"
        cursor.execute(sql, (id_usuario,))
        mysql.connection.commit()
        cursor.close()

    def desactivar_rostro(self, id_usuario):
        self.asegurar_columna_rostro()
        cursor = mysql.connection.cursor()

        sql = "UPDATE usuarios SET rostro_activo = 0 WHERE id_usuario = %s"
        cursor.execute(sql, (id_usuario,))
        mysql.connection.commit()
        cursor.close()
    
    def validar_login(self, usuario, password):
        self.asegurar_columna_rostro()
        cursor = mysql.connection.cursor()
        
        sql = """
        SELECT id_usuario, nombre, usuario, rostro_activo
        FROM usuarios 
        WHERE usuario = %s AND password = %s
        """
        
        cursor.execute(sql, (usuario, password))
        resultado = cursor.fetchone()
        cursor.close()
        
        return resultado 
