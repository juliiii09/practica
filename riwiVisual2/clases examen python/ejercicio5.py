# reportes_y_filtros.py
import csv, os
from datetime import datetime

CSV_FILE = "prestamos_avanzado.csv"
HEADER = ["prestamo_id","equipo_id","usuario","tipo_usuario","fecha_solicitud","fecha_inicio","fecha_fin","dias","retraso","estado"]

def leer():
    if not os.path.exists(CSV_FILE):
        print("Archivo no existe:", CSV_FILE); return []
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def filtrar_por_mes_anio(lista, mes=None, anio=None):
    res = []
    for p in lista:
        fs = p.get("fecha_solicitud","")
        if not fs: continue
        try:
            d = datetime.strptime(fs, "%Y-%m-%d")
        except:
            continue
        if mes and d.month != int(mes): continue
        if anio and d.year != int(anio): continue
        res.append(p)
    return res

def agrupar_por_estado(lista):
    resumen = {}
    for p in lista:
        est = p.get("estado","").upper() or "DESCONOCIDO"
        resumen[est] = resumen.get(est, 0) + 1
    return resumen

def promedio_retraso(lista):
    total = 0
    count = 0
    for p in lista:
        try:
            total += int(p.get("retraso","0") or 0)
            count += 1
        except:
            pass
    return (total / count) if count else 0

def menu():
    allp = leer()
    if not allp:
        print("No hay registros.")
        return
    while True:
        print("\n--- REPORTES Y FILTROS ---")
        print("1) Filtrar por mes/año")
        print("2) Agrupar por estado (conteo)")
        print("3) Promedio de retraso (filtrado opcional)")
        print("0) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            mes = input("Mes (1-12) o enter: ").strip() or None
            anio = input("Año (YYYY) o enter: ").strip() or None
            filtrados = filtrar_por_mes_anio(allp, mes, anio)
            for p in filtrados: print(p)
        elif op == "2":
            resumen = agrupar_por_estado(allp)
            print("Resumen por estado:", resumen)
        elif op == "3":
            mes = input("Mes (opcional): ").strip() or None
            anio = input("Año (opcional): ").strip() or None
            filtrados = filtrar_por_mes_anio(allp, mes, anio)
            print("Promedio retraso:", promedio_retraso(filtrados))
        elif op == "0":
            break
        else:
            print("Inválido")

if __name__ == "__main__":
    menu()

"""
Nombre archivo: reportes_y_filtros.py
Objetivo: cargar un CSV (ej. prestamos_avanzado.csv), filtrar por mes/año/estado/tipo_usuario, agrupar y mostrar resumen (conteos y totales)

"""