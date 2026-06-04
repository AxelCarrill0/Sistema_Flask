from flask_mysqldb import MySQL

mysql = MySQL()

def configurar_db(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'A001'
    app.config['MYSQL_DB'] = 'proyecto_flask'
    
    mysql.init_app(app)
