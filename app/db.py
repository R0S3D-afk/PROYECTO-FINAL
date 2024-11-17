import pymysql

def conexion():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="Jorge26Salazar",
        database="sistema_reparto",
        cursorclass=pymysql.cursors.DictCursor
    )
