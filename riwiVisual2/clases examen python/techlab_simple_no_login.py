# techlab_simple_no_login.py
# Versión MUY simple — sin autenticación — para probar ejecución en tu máquina.

import csv
from datetime import datetime, timedelta
import os

EQUIPOS_CSV = "equipos_simple.csv"
PRESTAMOS_CSV = "prestamos_simple.csv"

# Cabeceras
EQUIPOS_HEADER = ["equipo_id", "nombre_equipo", "categoria", "estado_actual", "fecha_registro"]
PRESTAMOS_HEADER = ["prestamo_id","equipo_id","nombre_equipo","usuario_prestatario","tipo_usuario","fecha_solicitud","fecha_inicio","fecha_fin","dias","retraso","estado","mes","anio"]

def asegurar(path, header):
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)

def leer_dicts(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def escribir_dicts(path, header, dicts):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for d in dicts:
            writer.writerow(d)

def append_dict(path, header, row):
    existe = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if not existe:
            writer.writeheader()
        writer.writerow(row)

def hoy_str():
    return datetime.now().strftime("%Y-%m-%d")

# Funciones simples para equipos
def generar_id_equipos(equipos):
    ids = []
    for e in equipos:
        try:
            ids.append(int(e.get("equipo_id", 0)))
        except:
            pass
    return str(max(ids)+1) if ids else "1"

def crear_equipo():
    equipos = leer_dicts(EQUIPOS_CSV)
    nuevo_id = generar_id_equipos(equipos)
    nombre = input("Nombre equipo: ").strip()
    categoria = input("Categoría: ").strip() or "Sin categoría"
    fila = {"equipo_id": nuevo_id, "nombre_equipo": nombre, "categoria": categoria, "estado_actual": "DISPONIBLE", "fecha_registro": hoy_str()}
    append_dict(EQUIPOS_CSV, EQUIPOS_HEADER, fila)
    print("Equipo creado:", fila)

def listar_equipos():
    for e in leer_dicts(EQUIPOS_CSV):
        print(e)

def buscar_equipo():
    q = input("ID o parte del nombre a buscar: ").strip()
    res = []
    for e in leer_dicts(EQUIPOS_CSV):
        if e["equipo_id"] == q or q.lower() in e["nombre_equipo"].lower():
            res.append(e)
    if not res:
        print("No encontrado.")
    else:
        for r in res:
            print(r)

def actualizar_estado_equipo():
    eid = input("ID equipo: ").strip()
    equipos = leer_dicts(EQUIPOS_CSV)
    cambiado = False
    for e in equipos:
        if e["equipo_id"] == eid:
            nuevo = input("Nuevo estado (DISPONIBLE/RESERVADO/PRESTADO): ").strip().upper()
            e["estado_actual"] = nuevo
            cambiado = True
            break
    if cambiado:
        escribir_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, equipos)
        print("Estado actualizado.")
    else:
        print("Equipo no encontrado.")

def eliminar_equipo():
    eid = input("ID a eliminar: ").strip()
    equipos = leer_dicts(EQUIPOS_CSV)
    nuevos = [e for e in equipos if e["equipo_id"] != eid]
    if len(nuevos) == len(equipos):
        print("No encontrado.")
    else:
        escribir_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, nuevos)
        print("Eliminado.")

# Funciones simples para préstamos
def generar_id_prestamos(prestamos):
    ids = []
    for p in prestamos:
        try:
            ids.append(int(p.get("prestamo_id", 0)))
        except:
            pass
    return str(max(ids)+1) if ids else "1"

TIEMPO_MAX = {"ESTUDIANTE":3, "INSTRUCTOR":7, "ADMINISTRATIVO":10}

def solicitar_prestamo():
    equipos = leer_dicts(EQUIPOS_CSV)
    eid = input("ID equipo a solicitar: ").strip()
    equipo = next((x for x in equipos if x["equipo_id"] == eid), None)
    if not equipo:
        print("Equipo no existe.")
        return
    if equipo.get("estado_actual","").upper() != "DISPONIBLE":
        print("No disponible.")
        return
    usuario = input("Nombre solicitante: ").strip()
    tipo = input("Tipo (Estudiante/Instructor/Administrativo): ").strip().upper() or "ESTUDIANTE"
    prestamos = leer_dicts(PRESTAMOS_CSV)
    pid = generar_id_prestamos(prestamos)
    fila = {"prestamo_id": pid, "equipo_id": eid, "nombre_equipo": equipo["nombre_equipo"], "usuario_prestatario": usuario, "tipo_usuario": tipo, "fecha_solicitud": hoy_str(), "fecha_inicio": "", "fecha_fin": "", "dias": "", "retraso": "", "estado": "PENDIENTE", "mes": datetime.now().strftime("%m"), "anio": datetime.now().strftime("%Y")}
    append_dict(PRESTAMOS_CSV, PRESTAMOS_HEADER, fila)
    # marcar reservado
    equipo["estado_actual"] = "RESERVADO"
    # guardar equipos actualizados
    equipos = [e if e["equipo_id"] != eid else equipo for e in equipos]
    escribir_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, equipos)
    print("Solicitud creada:", fila)

def listar_prestamos():
    for p in leer_dicts(PRESTAMOS_CSV):
        print(p)

def aprobar_prestamo():
    pid = input("ID préstamo a aprobar: ").strip()
    prestamos = leer_dicts(PRESTAMOS_CSV)
    cambiado = False
    for p in prestamos:
        if p["prestamo_id"] == pid and p["estado"].upper() == "PENDIENTE":
            inicio = hoy_str()
            dias = TIEMPO_MAX.get(p.get("tipo_usuario","").upper(), 3)
            fin = (datetime.strptime(inicio, "%Y-%m-%d") + timedelta(days=dias)).strftime("%Y-%m-%d")
            p["fecha_inicio"] = inicio
            p["fecha_fin"] = fin
            p["dias"] = str(dias)
            p["estado"] = "APROBADO"
            p["mes"] = datetime.now().strftime("%m")
            p["anio"] = datetime.now().strftime("%Y")
            cambiado = True
            # actualizar estado del equipo a PRESTADO
            equipos = leer_dicts(EQUIPOS_CSV)
            for e in equipos:
                if e["equipo_id"] == p["equipo_id"]:
                    e["estado_actual"] = "PRESTADO"
            escribir_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, equipos)
            break
    if cambiado:
        escribir_dicts(PRESTAMOS_CSV, PRESTAMOS_HEADER, prestamos)
        print("Aprobado.")
    else:
        print("No se aprobó (id/estado)")

def registrar_devolucion():
    pid = input("ID préstamo a devolver: ").strip()
    prestamos = leer_dicts(PRESTAMOS_CSV)
    cambiado = False
    for p in prestamos:
        if p["prestamo_id"] == pid and p["estado"].upper() == "APROBADO":
            if not p.get("fecha_inicio"):
                print("Registro inválido.")
                return
            inicio = datetime.strptime(p["fecha_inicio"], "%Y-%m-%d")
            dias_usados = (datetime.now() - inicio).days
            max_dias = TIEMPO_MAX.get(p.get("tipo_usuario","").upper(), 3)
            retraso = max(0, dias_usados - max_dias)
            p["dias"] = str(dias_usados)
            p["retraso"] = str(retraso)
            p["estado"] = "DEVUELTO"
            p["fecha_fin"] = hoy_str()
            p["mes"] = datetime.now().strftime("%m")
            p["anio"] = datetime.now().strftime("%Y")
            cambiado = True
            # actualizar equipo a DISPONIBLE
            equipos = leer_dicts(EQUIPOS_CSV)
            for e in equipos:
                if e["equipo_id"] == p["equipo_id"]:
                    e["estado_actual"] = "DISPONIBLE"
            escribir_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, equipos)
            break
    if cambiado:
        escribir_dicts(PRESTAMOS_CSV, PRESTAMOS_HEADER, prestamos)
        print("Devolución registrada.")
    else:
        print("No se pudo devolver (id/estado)")

def menu():
    asegurar(EQUIPOS_CSV, EQUIPOS_HEADER)
    asegurar(PRESTAMOS_CSV, PRESTAMOS_HEADER)
    while True:
        print("\\n--- MENU SIMPLE (sin login) ---")
        print("1) Crear equipo")
        print("2) Listar equipos")
        print("3) Buscar equipo")
        print("4) Editar estado")
        print("5) Eliminar equipo")
        print("6) Solicitar préstamo")
        print("7) Listar préstamos")
        print("8) Aprobar préstamo")
        print("9) Registrar devolución")
        print("0) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            crear_equipo()
        elif op == "2":
            listar_equipos()
        elif op == "3":
            buscar_equipo()
        elif op == "4":
            actualizar_estado_equipo()
        elif op == "5":
            eliminar_equipo()
        elif op == "6":
            solicitar_prestamo()
        elif op == "7":
            listar_prestamos()
        elif op == "8":
            aprobar_prestamo()
        elif op == "9":
            registrar_devolucion()
        elif op == "0":
            print("Saliendo. Adiós.")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()
