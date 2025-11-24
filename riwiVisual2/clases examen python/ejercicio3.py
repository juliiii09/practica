# prestamos_avanzado_fixed.py
# Versión del ejercicio 'Prestamos avanzado' con menú más tolerante:
# - acepta comandos en la misma línea (ej: '4 3')
# - o acepta sólo el número del comando (ej: '4') y luego pide el id
# - incluye backup automático antes de sobrescribir CSV

import csv, os, json
from datetime import datetime, timedelta
from shutil import copyfile

CSV_FILE = "prestamos_avanzado.csv"
JSON_REPORT = "prestamos_reporte.json"
HEADER = ["prestamo_id","equipo_id","usuario","tipo_usuario","fecha_solicitud","fecha_inicio","fecha_fin","dias","retraso","estado"]

TIEMPO_MAX = {"ESTUDIANTE":3, "INSTRUCTOR":7, "ADMINISTRATIVO":10}

def asegurar_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(HEADER)

def leer_prestamos():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def backup_csv():
    if os.path.exists(CSV_FILE):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        copia = f"backup_prestamos_{ts}.csv"
        copyfile(CSV_FILE, copia)
        print("Backup creado:", copia)

def escribir_prestamos(lista):
    backup_csv()
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        for r in lista:
            writer.writerow(r)

def generar_id(lista):
    ids = []
    for r in lista:
        try:
            ids.append(int(r.get("prestamo_id", 0)))
        except:
            pass
    return str(max(ids)+1) if ids else "1"

def crear_solicitud():
    lista = leer_prestamos()
    pid = generar_id(lista)
    equipo = input("ID equipo: ").strip()
    usuario = input("Nombre solicitante: ").strip()
    tipo = input("Tipo usuario (Estudiante/Instructor/Administrativo): ").strip().upper() or "ESTUDIANTE"
    fila = {
        "prestamo_id": pid,
        "equipo_id": equipo,
        "usuario": usuario,
        "tipo_usuario": tipo,
        "fecha_solicitud": datetime.now().strftime("%Y-%m-%d"),
        "fecha_inicio": "",
        "fecha_fin": "",
        "dias": "",
        "retraso": "",
        "estado": "PENDIENTE"
    }
    lista.append(fila)
    escribir_prestamos(lista)
    print("Solicitud creada:", fila)

def listar_todos():
    for p in leer_prestamos():
        print(p)

def listar_pendientes():
    pendientes = [p for p in leer_prestamos() if p.get("estado","").upper() == "PENDIENTE"]
    if not pendientes:
        print("No hay pendientes.")
        return
    for p in pendientes:
        print(p)

def aprobar(prestamo_id):
    prestamos = leer_prestamos()
    cambiado = False
    for p in prestamos:
        if p["prestamo_id"] == prestamo_id and p["estado"].upper() == "PENDIENTE":
            inicio = datetime.now().strftime("%Y-%m-%d")
            dias = TIEMPO_MAX.get(p.get("tipo_usuario","").upper(), 3)
            fin = (datetime.strptime(inicio, "%Y-%m-%d") + timedelta(days=dias)).strftime("%Y-%m-%d")
            p["fecha_inicio"] = inicio
            p["fecha_fin"] = fin
            p["dias"] = str(dias)
            p["estado"] = "APROBADO"
            cambiado = True
            break
    if cambiado:
        escribir_prestamos(prestamos)
        print("Aprobado:", prestamo_id)
    else:
        print("No se pudo aprobar (id/estado)")

def rechazar(prestamo_id):
    prestamos = leer_prestamos()
    for p in prestamos:
        if p["prestamo_id"] == prestamo_id and p["estado"].upper() == "PENDIENTE":
            p["estado"] = "RECHAZADO"
            escribir_prestamos(prestamos)
            print("Rechazado:", prestamo_id)
            return
    print("No se rechazó (id/estado)")

def registrar_devolucion(prestamo_id):
    prestamos = leer_prestamos()
    for p in prestamos:
        if p["prestamo_id"] == prestamo_id and p["estado"].upper() == "APROBADO":
            if not p.get("fecha_inicio"):
                print("Registro inválido: sin fecha_inicio")
                return
            inicio = datetime.strptime(p["fecha_inicio"], "%Y-%m-%d")
            dias_usados = (datetime.now() - inicio).days
            max_dias = TIEMPO_MAX.get(p.get("tipo_usuario","").upper(), 3)
            retraso = max(0, dias_usados - max_dias)
            p["dias"] = str(dias_usados)
            p["retraso"] = str(retraso)
            p["fecha_fin"] = datetime.now().strftime("%Y-%m-%d")
            p["estado"] = "DEVUELTO"
            escribir_prestamos(prestamos)
            print("Devolución registrada:", prestamo_id, "dias:", dias_usados, "retraso:", retraso)
            return
    print("No se pudo devolver (id/estado)")

def exportar_json():
    prestamos = leer_prestamos()
    with open(JSON_REPORT, "w", encoding="utf-8") as f:
        json.dump(prestamos, f, ensure_ascii=False, indent=2)
    print("Exportado a", JSON_REPORT)

# Menú tolerante: acepta '4 3' o '4' y luego pide id
def menu():
    asegurar_csv()
    while True:
        print("\n--- PRESTAMOS AVANZADO ---")
        print("1) Crear solicitud")
        print("2) Listar todos")
        print("3) Listar pendientes")
        print("4) Aprobar <id>")
        print("5) Rechazar <id>")
        print("6) Registrar devolución <id>")
        print("7) Exportar JSON")
        print("0) Salir")
        entrada = input("Opción (ej: 4 3 para aprobar id=3): ").strip()
        if not entrada:
            continue
        partes = entrada.split()
        cmd = partes[0]
        param = None
        # si solo se ingresó el comando y requiere id, pedimos id por separado
        if len(partes) == 1 and cmd in ("4", "5", "6"):
            param = input("Ingresa el id: ").strip()
        else:
            if len(partes) > 1:
                param = partes[1]

        if cmd == "1":
            crear_solicitud()
        elif cmd == "2":
            listar_todos()
        elif cmd == "3":
            listar_pendientes()
        elif cmd == "4":
            if param:
                aprobar(param)
            else:
                print("Falta el id para aprobar.")
        elif cmd == "5":
            if param:
                rechazar(param)
            else:
                print("Falta el id para rechazar.")
        elif cmd == "6":
            if param:
                registrar_devolucion(param)
            else:
                print("Falta el id para registrar devolución.")
        elif cmd == "7":
            exportar_json()
        elif cmd == "0":
            print("Saliendo...")
            break
        else:
            print("Comando inválido.")

if __name__ == "__main__":
    menu()


    
    
"""
#Ejemplo de ejecución por consola (flujo)
> python prestamos_avanzado.py
#--- PRESTAMOS AVANZADO ---
1) Crear solicitud
2) Listar todos
3) Listar pendientes
4) Aprobar <id>
...
Opción: 1
ID equipo: 5
Nombre solicitante: Ana
Tipo usuario (Estudiante/Instructor/Administrativo): Estudiante
Solicitud creada: {...}
Opción: 3
{...}  # muestra solicitud pendiente con prestamo_id = 1
Opción: 4 1
Aprobado: 1
Opción: 6 1
Devolución registrada: 1 dias: 4 retraso: 0
Opción: 7
Exportado a prestamos_reporte.json"""