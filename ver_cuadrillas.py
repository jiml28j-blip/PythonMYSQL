
import os
import pymysql

conexion = pymysql.connect(
    host="mysql-44e7c46-jiml28j-1ce9.e.aivencloud.com",
    user="avnadmin",
    password="AVNS_U7bEZriwYqpKxRHZhTy",
    database="defaultdb",
    port=13999,
    ssl={"fake_flag_to_enable_ssl": True}
)

try:
    with conexion.cursor() as cursor:
        print("--- LISTADO DE CUADRILLAS Y SUPERVISORES ---")
        cursor.execute("SELECT * FROM cuadrillas;")
        for fila in cursor.fetchall():
            print(fila)
            
        print("\n--- LISTADO DE UNIDADES ROTATIVAS ---")
        cursor.execute("SELECT * FROM unidades;")
        for fila in cursor.fetchall():
            print(fila)
finally:
    conexion.close()