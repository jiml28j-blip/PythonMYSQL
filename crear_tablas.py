import os
import pymysql

# Leemos tu contraseña de la variable de entorno
db_password = os.environ.get("DB_PASSWORD", "AVNS_U7bEZriwYqpKxRHZhTy")

def inicializar_base_datos():
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
            # 1. Crear la tabla de cuadrillas (supervisores y turnos fijos)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cuadrillas (
                    nombre_supervisor VARCHAR(100) PRIMARY KEY,
                    turno VARCHAR(50) NOT NULL,
                    baches_atendidos INT DEFAULT 0
                );
            """)
            
            # 2. Crear la tabla de unidades (vehículos rotativos)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS unidades (
                    numero_unidad VARCHAR(20) PRIMARY KEY,
                    estado VARCHAR(30) DEFAULT 'Disponible',
                    supervisor_asignado VARCHAR(100),
                    FOREIGN KEY (supervisor_asignado) REFERENCES cuadrillas(nombre_supervisor) ON DELETE SET NULL
                );
            """)
            
            print("¡Tablas 'cuadrillas' y 'unidades' creadas exitosamente!")
            
            # 3. Poblar las 13 cuadrillas iniciales
            cuadrillas_datos = [
                ("Supervisor Matutino 1", "Lunes a Viernes 06:00 - 14:00", 0),
                ("Supervisor Matutino 2", "Lunes a Viernes 06:00 - 14:00", 0),
                ("Supervisor Matutino 3", "Lunes a Viernes 06:00 - 14:00", 0),
                ("Supervisor Matutino 4", "Lunes a Viernes 06:00 - 14:00", 0),
                ("Supervisor Matutino 5", "Lunes a Viernes 06:00 - 14:00", 0),
                ("Supervisor Matutino 6", "Lunes a Viernes 06:00 - 14:00", 0),
                ("Supervisor Matutino 7", "Lunes a Viernes 06:00 - 14:00", 0),
                ("Supervisor Rotativo 8", "Miércoles a Domingo 06:00 - 14:00", 0),
                ("Supervisor Rotativo 9", "Miércoles a Domingo 06:00 - 14:00", 0),
                ("Supervisor Rotativo 10", "Miércoles a Domingo 06:00 - 14:00", 0),
                ("Supervisor Operativo 11", "Lunes a Viernes 06:00 - 14:00", 0),
                ("Supervisor Operativo 12", "Lunes a Viernes 06:00 - 14:00", 0),
                ("Supervisor Operativo 13", "Miércoles a Domingo 06:00 - 14:00", 0)
            ]
            
            sql_cuadrillas = """
                INSERT IGNORE INTO cuadrillas (nombre_supervisor, turno, baches_atendidos) 
                VALUES (%s, %s, %s);
            """
            cursor.executemany(sql_cuadrillas, cuadrillas_datos)
            
            # 4. Poblar las 6 unidades vehiculares rotativas
            unidades_datos = [
                ("CBA-015", "Disponible", None),
                ("CBA-153", "Disponible", None),
                ("CBA-801", "Disponible", None),
                ("CBA-455", "Disponible", None),
                ("CBA-571", "Disponible", None),
                ("CBA-235", "Disponible", None)
            ]
            
            sql_unidades = """
                INSERT IGNORE INTO unidades (numero_unidad, estado, supervisor_asignado) 
                VALUES (%s, %s, %s);
            """
            cursor.executemany(sql_unidades, unidades_datos)
            
            conexion.commit()
            print("¡Datos iniciales de cuadrillas y vehículos cargados correctamente!")
            
    finally:
        conexion.close()

if __name__ == "__main__":
    inicializar_base_datos()