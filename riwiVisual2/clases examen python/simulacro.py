



# usuarios.py (versión simple)
import csv
import getpass

USUARIOS_CSV = "usuarios.csv"
MAX_INTENTOS = 3

def cargar_usuarios():
    usuarios = []
    try:
        with open(USUARIOS_CSV, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # saltar cabecera
            for row in reader:
                # esperamos: usuario,contrasena,rol
                usuarios.append({"usuario": row[0].strip(), "contrasena": row[1].strip(), "rol": row[2].strip()})
    except FileNotFoundError:
        return []
    return usuarios

def autenticar():
    usuarios = cargar_usuarios()
    if not usuarios:
        print("No hay usuarios en usuarios.csv")
        return None
    intentos = 0
    while intentos < MAX_INTENTOS:
        u = input("Usuario: ").strip()
        p = getpass.getpass("Contraseña: ").strip()
        for usr in usuarios:
            if usr["usuario"] == u and usr["contrasena"] == p and usr["rol"].upper() == "ADMIN":
                print("Login exitoso.")
                return usr
        intentos += 1
        print("Credenciales incorrectas. Intentos restantes:", MAX_INTENTOS - intentos)
    print("Máximo intentos superado.")
    return None

###############################################


# equipos.py (versión simple)
import csv
from datetime import datetime

EQUIPOS_CSV = "equipos.csv"

def cargar_equipos():
    equipos = []
    try:
        with open(EQUIPOS_CSV, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # cabecera
            for row in reader:
                equipos.append({
                    "equipo_id": row[0],
                    "nombre_equipo": row[1],
                    "categoria": row[2],
                    "estado_actual": row[3],
                    "fecha_registro": row[4]
                })
    except FileNotFoundError:
        return []
    return equipos

def guardar_equipos(equipos):
    with open(EQUIPOS_CSV, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["equipo_id","nombre_equipo","categoria","estado_actual","fecha_registro"])
        for e in equipos:
            writer.writerow([e["equipo_id"], e["nombre_equipo"], e["categoria"], e["estado_actual"], e["fecha_registro"]])

def nuevo_equipo(nombre, categoria):
    equipos = cargar_equipos()
    nuevo_id = 1
    if equipos:
        try:
            ids = [int(e["equipo_id"]) for e in equipos]
            nuevo_id = max(ids) + 1
        except:
            nuevo_id = len(equipos) + 1
    fecha = datetime.now().strftime("%Y-%m-%d")
    equipo = {"equipo_id": str(nuevo_id), "nombre_equipo": nombre, "categoria": categoria, "estado_actual": "DISPONIBLE", "fecha_registro": fecha}
    equipos.append(equipo)
    guardar_equipos(equipos)
    return equipo

def buscar_equipo(equipo_id):
    for e in cargar_equipos():
        if e["equipo_id"] == str(equipo_id):
            return e
    return None

def listar():
    return cargar_equipos()

def cambiar_estado(equipo_id, estado):
    equipos = cargar_equipos()
    cambiado = False
    for e in equipos:
        if e["equipo_id"] == str(equipo_id):
            e["estado_actual"] = estado
            cambiado = True
            break
    if cambiado:
        guardar_equipos(equipos)
    return cambiado

###########################################################

# prestamos.py (versión simple)
import csv
from datetime import datetime, timedelta

PRESTAMOS_CSV = "prestamos.csv"

TIEMPO_MAX = {"ESTUDIANTE":3, "INSTRUCTOR":7, "ADMINISTRATIVO":10}

def cargar_prestamos():
    prestamos = []
    try:
        with open(PRESTAMOS_CSV, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                prestamos.append({
                    "prestamo_id": row[0],
                    "equipo_id": row[1],
                    "nombre_equipo": row[2],
                    "usuario_prestatario": row[3],
                    "tipo_usuario": row[4],
                    "fecha_solicitud": row[5],
                    "fecha_inicio": row[6],
                    "fecha_fin": row[7],
                    "dias": row[8],
                    "retraso": row[9],
                    "estado": row[10],
                    "mes": row[11],
                    "anio": row[12]
                })
    except FileNotFoundError:
        return []
    return prestamos

def guardar_prestamos(prestamos):
    with open(PRESTAMOS_CSV, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["prestamo_id","equipo_id","nombre_equipo","usuario_prestatario","tipo_usuario","fecha_solicitud","fecha_inicio","fecha_fin","dias","retraso","estado","mes","anio"])
        for p in prestamos:
            writer.writerow([p[k] for k in ["prestamo_id","equipo_id","nombre_equipo","usuario_prestatario","tipo_usuario","fecha_solicitud","fecha_inicio","fecha_fin","dias","retraso","estado","mes","anio"]])

def nuevo_prestamo(equipo_id, nombre_equipo, usuario, tipo):
    prestamos = cargar_prestamos()
    nuevo_id = 1
    if prestamos:
        try:
            ids = [int(p["prestamo_id"]) for p in prestamos]
            nuevo_id = max(ids) + 1
        except:
            nuevo_id = len(prestamos) + 1
    hoy = datetime.now()
    p = {
        "prestamo_id": str(nuevo_id),
        "equipo_id": str(equipo_id),
        "nombre_equipo": nombre_equipo,
        "usuario_prestatario": usuario,
        "tipo_usuario": tipo.upper(),
        "fecha_solicitud": hoy.strftime("%Y-%m-%d"),
        "fecha_inicio": "",
        "fecha_fin": "",
        "dias": "",
        "retraso": "",
        "estado": "PENDIENTE",
        "mes": hoy.strftime("%m"),
        "anio": hoy.strftime("%Y")
    }
    prestamos.append(p)
    guardar_prestamos(prestamos)
    return p

def listar_pendientes():
    return [p for p in cargar_prestamos() if p["estado"] == "PENDIENTE"]

def aprobar(prestamo_id):
    prestamos = cargar_prestamos()
    for p in prestamos:
        if p["prestamo_id"] == str(prestamo_id) and p["estado"] == "PENDIENTE":
            inicio = datetime.now()
            dias = TIEMPO_MAX.get(p["tipo_usuario"].upper(), 3)
            fin = inicio + timedelta(days=dias)
            p["fecha_inicio"] = inicio.strftime("%Y-%m-%d")
            p["fecha_fin"] = fin.strftime("%Y-%m-%d")
            p["dias"] = str(dias)
            p["estado"] = "APROBADO"
            p["mes"] = inicio.strftime("%m")
            p["anio"] = inicio.strftime("%Y")
            guardar_prestamos(prestamos)
            return True
    return False

def rechazar(prestamo_id):
    prestamos = cargar_prestamos()
    for p in prestamos:
        if p["prestamo_id"] == str(prestamo_id) and p["estado"] == "PENDIENTE":
            p["estado"] = "RECHAZADO"
            guardar_prestamos(prestamos)
            return True
    return False

def devolver(prestamo_id):
    prestamos = cargar_prestamos()
    for p in prestamos:
        if p["prestamo_id"] == str(prestamo_id) and p["estado"] == "APROBADO":
            if not p["fecha_inicio"]:
                return False
            inicio = datetime.strptime(p["fecha_inicio"], "%Y-%m-%d")
            hoy = datetime.now()
            dias_usados = (hoy - inicio).days
            max_dias = TIEMPO_MAX.get(p["tipo_usuario"].upper(), 3)
            retraso = dias_usados - max_dias
            if retraso < 0:
                retraso = 0
            p["dias"] = str(dias_usados)
            p["retraso"] = str(retraso)
            p["estado"] = "DEVUELTO"
            p["fecha_fin"] = hoy.strftime("%Y-%m-%d")
            p["mes"] = hoy.strftime("%m")
            p["anio"] = hoy.strftime("%Y")
            guardar_prestamos(prestamos)
            return True
    return False

def por_usuario(usuario):
    return [p for p in cargar_prestamos() if p["usuario_prestatario"] == usuario]

def por_equipo(equipo_id):
    return [p for p in cargar_prestamos() if p["equipo_id"] == str(equipo_id)]


##########################################

# reportes.py (simple)
import csv
from prestamos import cargar_prestamos

def exportar_mensual(mes, anio, archivo_salida):
    prestamos = cargar_prestamos()
    mes = f"{int(mes):02d}"
    filtrados = [p for p in prestamos if p["mes"] == mes and p["anio"] == str(anio)]
    if not filtrados:
        return False, "No hay registros."
    with open(archivo_salida, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["prestamo_id","equipo_id","nombre_equipo","usuario_prestatario","tipo_usuario","fecha_solicitud","fecha_inicio","fecha_fin","dias","retraso","estado","mes","anio"])
        for p in filtrados:
            writer.writerow([p[k] for k in ["prestamo_id","equipo_id","nombre_equipo","usuario_prestatario","tipo_usuario","fecha_solicitud","fecha_inicio","fecha_fin","dias","retraso","estado","mes","anio"]])
    return True, f"Exportado {len(filtrados)} registros."

def exportar_anual(anio, archivo_salida):
    prestamos = cargar_prestamos()
    filtrados = [p for p in prestamos if p["anio"] == str(anio)]
    if not filtrados:
        return False, "No hay registros."
    with open(archivo_salida, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["prestamo_id","equipo_id","nombre_equipo","usuario_prestatario","tipo_usuario","fecha_solicitud","fecha_inicio","fecha_fin","dias","retraso","estado","mes","anio"])
        for p in filtrados:
            writer.writerow([p[k] for k in ["prestamo_id","equipo_id","nombre_equipo","usuario_prestatario","tipo_usuario","fecha_solicitud","fecha_inicio","fecha_fin","dias","retraso","estado","mes","anio"]])
    return True, f"Exportado {len(filtrados)} registros."

##################################################################

# utils.py
def menu_principal():
    print("\n--- MENU PRINCIPAL ---")
    print("1) Equipos")
    print("2) Solicitar préstamo")
    print("3) Revisar pendientes")
    print("4) Registrar devolución")
    print("5) Reportes")
    print("6) Salir")

def menu_equipos():
    print("\n--- GESTION EQUIPOS ---")
    print("1) Nuevo equipo")
    print("2) Listar equipos")
    print("3) Buscar por ID")
    print("4) Volver")


#############################################################

# main.py (versión simple)
from usuarios import autenticar
from equipos import nuevo_equipo, listar, buscar_equipo, cambiar_estado
from prestamos import nuevo_prestamo, listar_pendientes, aprobar, rechazar, devolver, por_equipo
from reportes import exportar_mensual, exportar_anual
from utils import menu_principal, menu_equipos

def inicio():
    print("=== TechLab - Consola ===")
    user = autenticar()
    if not user:
        return
    while True:
        menu_principal()
        opc = input("Opción: ").strip()
        if opc == "1":
            while True:
                menu_equipos()
                e = input("Opción equipos: ").strip()
                if e == "1":
                    nombre = input("Nombre: ")
                    categoria = input("Categoría: ")
                    equipo = nuevo_equipo(nombre, categoria)
                    print("Equipo creado:", equipo)
                elif e == "2":
                    for eq in listar():
                        print(eq)
                elif e == "3":
                    eid = input("ID: ")
                    print(buscar_equipo(eid) or "No encontrado")
                elif e == "4":
                    break
                else:
                    print("Opción inválida")
        elif opc == "2":
            eid = input("ID equipo a pedir: ")
            equipo = buscar_equipo(eid)
            if not equipo:
                print("Equipo no existe")
            elif equipo["estado_actual"] != "DISPONIBLE":
                print("No disponible")
            else:
                nombre = input("Nombre solicitante: ")
                tipo = input("Tipo (Estudiante/Instructor/Administrativo): ")
                p = nuevo_prestamo(eid, equipo["nombre_equipo"], nombre, tipo)
                cambiar_estado(eid, "RESERVADO")
                print("Solicitud creada:", p)
        elif opc == "3":
            pend = listar_pendientes()
            if not pend:
                print("No hay pendientes")
            else:
                for p in pend:
                    print(p)
                accion = input("Aprobar(A)<id> / Rechazar(R)<id> / V para volver: ").strip()
                if accion.upper().startswith("A"):
                    pid = accion[1:].strip()
                    if aprobar(pid):
                        # buscar préstamo aprobado para saber equipo y marcar estado PRESTADO
                        ps = por_equipo(None)  # no necesitamos esto aquí; en simple: buscamos manualmente
                        # mejor: buscar préstamo en archivo:
                        from prestamos import cargar_prestamos
                        allp = cargar_prestamos()
                        target = next((x for x in allp if x["prestamo_id"] == pid), None)
                        if target:
                            cambiar_estado(target["equipo_id"], "PRESTADO")
                        print("Aprobado", pid)
                    else:
                        print("No se aprobó")
                elif accion.upper().startswith("R"):
                    pid = accion[1:].strip()
                    if rechazar(pid):
                        from prestamos import cargar_prestamos
                        allp = cargar_prestamos()
                        target = next((x for x in allp if x["prestamo_id"] == pid), None)
                        if target:
                            cambiar_estado(target["equipo_id"], "DISPONIBLE")
                        print("Rechazado", pid)
                    else:
                        print("No se rechazó")
        elif opc == "4":
            pid = input("ID préstamo a devolver: ").strip()
            if devolver(pid):
                from prestamos import cargar_prestamos
                allp = cargar_prestamos()
                target = next((x for x in allp if x["prestamo_id"] == pid), None)
                if target:
                    cambiar_estado(target["equipo_id"], "DISPONIBLE")
                print("Devolución registrada")
            else:
                print("No se pudo registrar devolución")
        elif opc == "5":
            t = input("Mensual(M) o Anual(A): ").strip().upper()
            if t == "M":
                mes = input("Mes (1-12): ")
                anio = input("Año (YYYY): ")
                ok, msg = exportar_mensual(mes, anio, f"reporte_{anio}_{mes}.csv")
                print(msg)
            elif t == "A":
                anio = input("Año (YYYY): ")
                ok, msg = exportar_anual(anio, f"reporte_{anio}.csv")
                print(msg)
            else:
                print("Opción inválida")
        elif opc == "6":
            print("Adiós")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    inicio()




"""

usuarios.csv----------

usuario,contrasena,rol
admin,admin123,ADMIN

equipos.csv----------

equipo_id,nombre_equipo,categoria,estado_actual,fecha_registro
1,Portatil A,Computo,DISPONIBLE,2025-01-01







"""