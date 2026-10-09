import os
import pymysql

# Leemos la contraseña de forma segura desde las variables de entorno
db_password = os.environ.get("DB_PASSWORD", "AVNS_U7bEZriwYqpKxRHZhTy")

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
        cursor.execute("DESCRIBE registro;")
        columnas = cursor.fetchall()
        print("Columnas de la tabla 'registro':")
        for col in columnas:
            print(col)
finally:
    conexion.close()