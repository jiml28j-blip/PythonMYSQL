import os
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de Aiven usando una variable de entorno para la contraseña (más seguro para GitHub y Render)
db_password = os.environ.get("DB_PASSWORD", "AVNS_U7bEZriwYqpKxRHZhTy")
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://avnadmin:{db_password}@mysql-44e7c46-jiml28j'
    '-1ce9.e.aivencloud.com:13999/defaultdb'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Pasar el parámetro SSL requerido para Aiven de forma nativa
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'ssl': {'ssl_mode': 'REQUIRED'}}
}

db = SQLAlchemy(app)


# Definición del modelo basado en tu tabla existente 'registro'
class Registro(db.Model):
    __tablename__ = 'registro'
    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(200), nullable=False)


# Asegurar el contexto de la aplicación para verificar/crear tablas
with app.app_context():
    db.create_all()


# Ruta principal: Muestra el mensaje de bienvenida y lista los registros de la base de datos
@app.route('/')
def home():
    # Consultamos todos los registros almacenados en la tabla 'registro'
    registros = Registro.query.all()

    # HTML básico integrado para visualizar el listado y un formulario de prueba
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Sistema de Folios - Aiven</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; color: #333; }
            h1 { color: #0275d8; }
            ul { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 600px; }
            li { padding: 8px 0; border-bottom: 1px solid #eee; }
            form { margin-top: 20px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 600px; }
            input[type="text"] { width: 75%; padding: 8px; margin-right: 10px; border: 1px solid #ccc; border-radius: 4px; }
            input[type="submit"] { padding: 8px 15px; background-color: #5cb85c; color: white; border: none; border-radius: 4px; cursor: pointer; }
            input[type="submit"]:hover { background-color: #4cae4c; }
        </style>
    </head>
    <body>
        <h1>¡Conectado exitosamente a la base de datos en Aiven! </h1>
        
        <h3>Registros actuales en la tabla:</h3>
        <ul>
    """

    if registros:
        for reg in registros:
            html += f'<li><b>ID {reg.id}:</b> {reg.mensaje}</li>'
    else:
        html += '<li>No hay registros guardados todavía.</li>'

    html += """
        </ul>

        <form action="/agregar" method="POST">
            <h3>Agregar un nuevo folio/mensaje:</h3>
            <input type="text" name="mensaje" placeholder="Escribe el reporte o mensaje..." required>
            <input type="submit" value="Guardar Registro">
        </form>
    </body>
    </html>
    """
    return html


# Ruta para procesar la inserción de nuevos registros mediante POST
@app.route('/agregar', methods=['POST'])
def agregar():
    nuevo_mensaje = request.form.get('mensaje')
    if nuevo_mensaje:
        # Creamos una nueva instancia del modelo Registro
        nuevo_registro = Registro(mensaje=nuevo_mensaje)
        db.session.add(nuevo_registro)
        db.session.commit()  # Guardamos los cambios permanentemente en Aiven
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)