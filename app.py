import os
from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def conectar_bd():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', "mysql-44e7c46-jiml28j-1ce9.e.aivencloud.com"),
        user=os.environ.get('DB_USER', "avnadmin"),
        password=os.environ.get('DB_PASSWORD', "AVNS_U7bEZriwYqpKxRHZhTy"),
        database=os.environ.get('DB_NAME', "defaultdb"),
        port=int(os.environ.get('DB_PORT', 13999)),
        ssl={"fake_flag_to_enable_ssl": True}
    )

@app.route('/')
def index():
    # Consultar el estado de las unidades para mostrarlas en la web
    conexion = conectar_bd()
    unidades = []
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT numero_unidad, estado, supervisor_asignado FROM unidades;")
            unidades = cursor.fetchall()
    finally:
        conexion.close()
    
    # Aquí puedes renderizar una plantilla HTML pasándole las unidades
    # Por ahora, para probar que conecta, retornamos un texto plano:
    resultado = "<h1>Flotilla de Unidades (Aiven MySQL)</h1><ul>"
    for unidad, estado, supervisor in unidades:
        sup_txt = supervisor if supervisor else "Ninguno (Estacionada)"
        resultado += f"<li>🚗 {unidad} - Estado: <b>{estado}</b> - Asignada a: {sup_txt}</li>"
    resultado += "</ul>"
    return resultado

@app.route('/asignar', methods=['POST'])
def asignar():
    # Recibe los datos desde un formulario web en lugar de la terminal
    supervisor = request.form.get('supervisor')
    numero_unidad = request.form.get('numero_unidad')
    
    conexion = conectar_bd()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT estado FROM unidades WHERE numero_unidad = %s;", (numero_unidad,))
            res = cursor.fetchone()
            if res and res[0] == 'Disponible':
                cursor.execute("""
                    UPDATE unidades 
                    SET supervisor_asignado = %s, estado = 'Asignada' 
                    WHERE numero_unidad = %s;
                """, (supervisor, numero_unidad))
                conexion.commit()
    finally:
        conexion.close()
        
    return redirect(url_for('index'))

@app.route('/liberar/<numero_unidad>', methods=['POST'])
def liberar(numero_unidad):
    conexion = conectar_bd()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE unidades 
                SET supervisor_asignado = NULL, estado = 'Disponible' 
                WHERE numero_unidad = %s;
            """, (numero_unidad,))
            conexion.commit()
    finally:
        conexion.close()
        
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)