import os
import pymysql

def conectar_bd():
    return pymysql.connect(
        host="mysql-44e7c46-jiml28j-1ce9.e.aivencloud.com",
        user="avnadmin",
        password="AVNS_U7bEZriwYqpKxRHZhTy",
        database="defaultdb",
        port=13999,
        ssl={"fake_flag_to_enable_ssl": True}
    )

def ver_estado_unidades():
    conexion = conectar_bd()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT numero_unidad, estado, supervisor_asignado FROM unidades;")
            print("\n========================================")
            print("      ESTADO ACTUAL DE LA FLOTILLA      ")
            print("========================================")
            for unidad, estado, supervisor in cursor.fetchall():
                sup_txt = supervisor if supervisor else "Ninguno (Estacionada)"
                print(f"🚗 {unidad} -> [{estado}] | Asignada a: {sup_txt}")
            print("========================================")
    finally:
        conexion.close()

def asignar_vehiculo(supervisor, numero_unidad):
    conexion = conectar_bd()
    try:
        with conexion.cursor() as cursor:
            # Verificar si la unidad existe y está disponible
            cursor.execute("SELECT estado FROM unidades WHERE numero_unidad = %s;", (numero_unidad,))
            res = cursor.fetchone()
            
            if not res:
                print(f"\n❌ Error: La unidad {numero_unidad} no existe en el catálogo.")
                return
            
            if res[0] == 'Disponible':
                cursor.execute("""
                    UPDATE unidades 
                    SET supervisor_asignado = %s, estado = 'Asignada' 
                    WHERE numero_unidad = %s;
                """, (supervisor, numero_unidad))
                conexion.commit()
                print(f"\n✅ ¡Éxito! Vehículo {numero_unidad} asignado correctamente a '{supervisor}'.")
            else:
                print(f"\n⚠️ El vehículo {numero_unidad} ya se encuentra ocupado.")
    finally:
        conexion.close()

def liberar_vehiculo(numero_unidad):
    conexion = conectar_bd()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE unidades 
                SET supervisor_asignado = NULL, estado = 'Disponible' 
                WHERE numero_unidad = %s;
            """, (numero_unidad,))
            conexion.commit()
            print(f"\n✅ ¡Éxito! Vehículo {numero_unidad} liberado y devuelto al estacionamiento.")
    finally:
        conexion.close()

if __name__ == "__main__":
    while True:
        print("\n--- MENÚ DE GESTIÓN DE UNIDADES ---")
        print("1. Ver estado de vehículos")
        print("2. Asignar vehículo a un supervisor")
        print("3. Liberar vehículo")
        print("4. Salir")
        
        opcion = input("Elige una opción (1-4): ")
        
        if opcion == "1":
            ver_estado_unidades()
        elif opcion == "2":
            ver_estado_unidades()
            sup = input("\nEscribe el nombre exacto del supervisor (ej. Supervisor Matutino 1): ")
            uni = input("Escribe el número de unidad a asignar (ej. CBA-015): ")
            asignar_vehiculo(sup, uni)
        elif opcion == "3":
            ver_estado_unidades()
            uni = input("\nEscribe el número de unidad a liberar (ej. CBA-015): ")
            liberar_vehiculo(uni)
        elif opcion == "4":
            print("\nSaliendo del gestor. ¡Excelente avance con el sistema!")
            break
        else:
            print("\n⚠️ Opción no válida. Intenta de nuevo.") 