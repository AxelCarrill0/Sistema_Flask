import mysql.connector as db_connector

class MySQLWrapper:
    def __init__(self):
        self._connection = None

    @property
    def connection(self):
        if self._connection is None or not self._connection.is_connected():
            self._connection = db_connector.connect(
                host='localhost',
                user='root',
                password='A001',
                database='proyecto_flask'
            )
        return self._connection


mysql = MySQLWrapper()
