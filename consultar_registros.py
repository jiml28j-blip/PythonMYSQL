import os
import pymysql

# Leemos la contraseña usando un marcador seguro
db_password = os.environ.get("DB_PASSWORD", "TU_CONTRASENA_AQUI")

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
        cursor.execute("SELECT * FROM registro;")
        resultados = cursor.fetchall()
        
        print("Registros guardados en la tabla:")
        for fila in resultados:
            print(fila)
finally:
    conexion.close()