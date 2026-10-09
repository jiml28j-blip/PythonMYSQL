import os
import pymysql

# Leemos la contraseña exclusivamente de la variable de entorno
db_password = os.environ.get("DB_PASSWORD")

conexion = pymysql.connect(
    host="mysql-44e7c46-jiml28j-1ce9.e.aivencloud.com",
    user="avnadmin",
    password=db_password,
    database="defaultdb",
    port=13999,
    ssl={"fake_flag_to_enable_ssl": True}
)

try:
    with conexion.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tablas = cursor.fetchall()
        print("Tablas en la base de datos:")
        for tabla in tablas:
            print(tabla)
finally:
    conexion.close()