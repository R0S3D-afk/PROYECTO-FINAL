import pymysql

def conexion():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Jorge26Salazar",
        database="sistema_reparto",
        cursorclass=pymysql.cursors.DictCursor
    )
