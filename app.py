import os
from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Leemos la contraseña usando un marcador seguro por defecto para desarrollo local
db_password = os.environ.get("DB_PASSWORD", "TU_CONTRASENA_AQUI")

def get_db_connection():
    connection = pymysql.connect(
        host="mysql-44e7c46-jiml28j-1ce9.e.aivencloud.com",
        user="avnadmin",
        password=db_password,
        database="defaultdb",
        port=13999,
        ssl={"fake_flag_to_enable_ssl": True}
    )
    return connection

@app.route('/')
def home():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM registro;")
            registros = cursor.fetchall()
        connection.close()
    except Exception as e:
        registros = []
        print(f"Error al conectar a la BD: {e}")

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Sistema de Folios</title>
    </head>
    <body>
        <h1>Sistema de Control y Registro de Folios</h1>
        <form action="/agregar" method="POST">
            <input type="text" name="mensaje" placeholder="Escribe el reporte o mensaje..." required>
            <input type="submit" value="Guardar Registro">
        </form>
        <h2>Registros Guardados:</h2>
        <ul>
    """
    for reg in registros:
        html += f"<li>{reg}</li>"
    html += """
        </ul>
    </body>
    </html>
    """
    return html

@app.route('/agregar', methods=['POST'])
def agregar():
    mensaje = request.form['mensaje']
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO registro (mensaje) VALUES (%s);", (mensaje,))
            connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error al insertar: {e}")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)