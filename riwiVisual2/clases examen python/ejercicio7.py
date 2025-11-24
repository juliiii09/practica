"""
Objetivo: practicar 8 tareas en 2 horas; incluye datos de prueba y respuestas esperadas para autoevaluarte.

Enunciado (resumen)

Tarea 1: Crear 5 equipos (proveer datos).

Tarea 2: Crear 3 solicitudes de préstamo.

Tarea 3: Aprobar 2 solicitudes.

Tarea 4: Registrar devolución de 1 préstamo con retraso (simula fecha_inicio antigua).

Tarea 5: Generar reporte de préstamos por estado.

Tarea 6: Exportar préstamos a JSON.

Tarea 7: Crear backup del CSV.

Tarea 8: Restaurar backup y verificar integridad.

"""
# examen_simulado.py - script de pruebas automatizadas para practicar
from datetime import datetime, timedelta
import json, csv, os
# asume que tienes funciones crear_equipo, crear_solicitud, aprobar_prestamo, devolver_prestamo del app
# aquí hacemos un pseudo-run: crear datos directos en CSV para la práctica.

# 1) crear equipos de ejemplo
equipos = [
    {"equipo_id":"1","nombre_equipo":"Portatil A","categoria":"Computo","estado_actual":"DISPONIBLE","fecha_registro":"2025-01-01"},
    {"equipo_id":"2","nombre_equipo":"Camara","categoria":"Multimedia","estado_actual":"DISPONIBLE","fecha_registro":"2025-01-01"},
    {"equipo_id":"3","nombre_equipo":"Microscopio","categoria":"Lab","estado_actual":"DISPONIBLE","fecha_registro":"2025-01-01"}
]
# escribir CSV manualmente (útil para test rápido)
with open("equipos_test.csv","w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["equipo_id","nombre_equipo","categoria","estado_actual","fecha_registro"])
    w.writeheader()
    for e in equipos: w.writerow(e)
print("Equipos creados (archivo equipos_test.csv)")

# 2) crear prestamos de prueba: algunos con fecha_inicio antigua para forzar retraso
prestamos = []
hoy = datetime.now()
# préstamo 1: pendiente
prestamos.append({"prestamo_id":"1","equipo_id":"1","usuario":"Ana","tipo_usuario":"ESTUDIANTE","fecha_solicitud":hoy.strftime("%Y-%m-%d"),"fecha_inicio":"","fecha_fin":"","dias":"","retraso":"","estado":"PENDIENTE"})
# préstamo 2: aprobado y viejo (fecha_inicio hace 10 dias -> retraso)
inicio_viejo = (hoy - timedelta(days=10)).strftime("%Y-%m-%d")
prestamos.append({"prestamo_id":"2","equipo_id":"2","usuario":"Luis","tipo_usuario":"ESTUDIANTE","fecha_solicitud":hoy.strftime("%Y-%m-%d"),"fecha_inicio":inicio_viejo,"fecha_fin":"","dias":"3","retraso":"","estado":"APROBADO"})
# préstamo 3: aprobado reciente
inicio_reciente = (hoy - timedelta(days=1)).strftime("%Y-%m-%d")
prestamos.append({"prestamo_id":"3","equipo_id":"3","usuario":"María","tipo_usuario":"INSTRUCTOR","fecha_solicitud":hoy.strftime("%Y-%m-%d"),"fecha_inicio":inicio_reciente,"fecha_fin":"","dias":"7","retraso":"","estado":"APROBADO"})

with open("prestamos_test.csv","w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["prestamo_id","equipo_id","usuario","tipo_usuario","fecha_solicitud","fecha_inicio","fecha_fin","dias","retraso","estado"])
    w.writeheader()
    for p in prestamos: w.writerow(p)
print("Prestamos creados (prestamos_test.csv)")

# 3) ahora simular devolver el prestamo 2 y calcular retraso:
# (este bloque te sirve como plantilla para tu función registrar_devolucion)
def procesar_devolucion_csv(prestamo_id, csv_path="prestamos_test.csv"):
    rows=[]
    import csv
    from datetime import datetime
    with open(csv_path,newline="",encoding="utf-8") as f:
        R = list(csv.DictReader(f))
    for r in R:
        if r["prestamo_id"]==prestamo_id and r["estado"]=="APROBADO":
            inicio = datetime.strptime(r["fecha_inicio"], "%Y-%m-%d")
            dias_usados = (datetime.now() - inicio).days
            max_dias = 3 if r["tipo_usuario"].upper()=="ESTUDIANTE" else 7
            retraso = max(0, dias_usados - max_dias)
            r["dias"] = str(dias_usados); r["retraso"] = str(retraso)
            r["fecha_fin"] = datetime.now().strftime("%Y-%m-%d")
            r["estado"] = "DEVUELTO"
        rows.append(r)
    with open(csv_path,"w",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=R[0].keys()); w.writeheader(); [w.writerow(x) for x in rows]
    print("Devolución procesada:", prestamo_id)

procesar_devolucion_csv("2")
print("Revisa prestamos_test.csv para ver dias y retraso calculado.")

e