# school_grading_system.py
# Sistema escolar: estudiantes, asignaturas, notas, promedios ponderados

import csv, os, json
from statistics import mean

STUDENTS_CSV = "estudiantes.csv"
SUBJECTS_CSV = "asignaturas.csv"
NOTES_CSV = "notas.csv"

STUDENTS_HEADER = ["student_id","name"]
SUBJECTS_HEADER = ["subject_id","name","weight"]
NOTES_HEADER = ["note_id","student_id","subject_id","nota","tipo"]

def asegurar(path, header):
    if not os.path.exists(path):
        with open(path,"w",newline="",encoding="utf-8") as f: csv.writer(f).writerow(header)

def read(path):
    if not os.path.exists(path): return []
    with open(path,newline="",encoding="utf-8") as f: return list(csv.DictReader(f))

def write(path, header, rows):
    with open(path,"w",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header); w.writeheader(); [w.writerow(r) for r in rows]

def append(path, header, row):
    ex = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path,"a",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header)
        if not ex: w.writeheader()
        w.writerow(row)

def next_id(rows, key):
    ids=[]
    for r in rows:
        try: ids.append(int(r[key])); except: pass
    return str(max(ids)+1) if ids else "1"

# CRUD basico: estudiantes y asignaturas
def add_student():
    s = read(STUDENTS_CSV); sid = next_id(s,"student_id"); name = input("Nombre estudiante: ").strip()
    append(STUDENTS_CSV, STUDENTS_HEADER, {"student_id":sid,"name":name}); print("Estudiante agregado")

def add_subject():
    s = read(SUBJECTS_CSV); sid = next_id(s,"subject_id"); name = input("Nombre asignatura: ").strip()
    w = float(input("Peso (ej 0.25): ").strip() or "0")
    append(SUBJECTS_CSV, SUBJECTS_HEADER, {"subject_id":sid,"name":name,"weight":str(w)}); print("Asignatura agregada")

def add_note():
    notes = read(NOTES_CSV); nid = next_id(notes,"note_id")
    student_id = input("ID estudiante: ").strip(); subject_id = input("ID asignatura: ").strip()
    nota = float(input("Nota (0-5): ").strip() or "0")
    if nota < 0 or nota > 5: print("Nota fuera de rango"); return
    tipo = input("Tipo (PARCIAL/FINAL/TAREA): ").strip().upper() or "PARCIAL"
    append(NOTES_CSV, NOTES_HEADER, {"note_id":nid,"student_id":student_id,"subject_id":subject_id,"nota":str(nota),"tipo":tipo})
    print("Nota agregada")

# Calculo de promedios ponderados por estudiante
def calcular_promedio_estudiante(student_id):
    subjects = read(SUBJECTS_CSV)
    notes = read(NOTES_CSV)
    # construir dict de pesos
    pesos = {s["subject_id"]: float(s.get("weight",0)) for s in subjects}
    # si la suma de pesos no es 1, normalizamos
    total_pesos = sum(pesos.values())
    if total_pesos == 0:
        # asignacion uniforme
        n = len(subjects) if subjects else 1
        pesos = {sid: 1/n for sid in pesos}
        total_pesos = 1
    elif abs(total_pesos - 1.0) > 1e-6:
        # normalizar
        pesos = {k: v/total_pesos for k,v in pesos.items()}

    # promedio por asignatura (media de notas por asignatura)
    notas_por_subj = {}
    for n in notes:
        if n["student_id"] != student_id: continue
        subj = n["subject_id"]
        notas_por_subj.setdefault(subj, []).append(float(n["nota"]))
    # calcular promedio ponderado
    acumulado = 0.0
    for subj, weight in pesos.items():
        subj_prom = mean(notas_por_subj.get(subj, [0])) if notas_por_subj.get(subj) else 0
        acumulado += subj_prom * weight
    return acumulado

def report_student(student_id):
    students = read(STUDENTS_CSV)
    s = next((x for x in students if x["student_id"]==student_id), None)
    if not s:
        print("Estudiante no existe"); return
    prom = calcular_promedio_estudiante(student_id)
    estado = "APROBADO" if prom >= 3.5 else "REPROBADO"
    print(f"Reporte de {s['name']} (id {student_id}): Promedio={prom:.2f} Estado={estado}")

# Exportar reportes para todos
def export_all_reports():
    students = read(STUDENTS_CSV)
    rows = []
    for st in students:
        prom = calcular_promedio_estudiante(st["student_id"])
        estado = "APROBADO" if prom >= 3.5 else "REPROBADO"
        rows.append({"student_id": st["student_id"], "name": st["name"], "promedio": f"{prom:.2f}", "estado": estado})
    # exportar CSV
    with open("reportes_estudiantes.csv","w",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["student_id","name","promedio","estado"]); w.writeheader(); [w.writerow(r) for r in rows]
    print("Exportados reportes_estudiantes.csv")

# Menu
def menu():
    asegurar(STUDENTS_CSV, STUDENTS_HEADER); asegurar(SUBJECTS_CSV, SUBJECTS_HEADER); asegurar(NOTES_CSV, NOTES_HEADER)
    while True:
        print("\\n--- SISTEMA DE NOTAS ---")
        print("1) Agregar estudiante 2) Agregar asignatura 3) Agregar nota 4) Reporte estudiante 5) Exportar reportes 0) Salir")
        op = input("Opción: ").strip()
        if op=="1": add_student()
        elif op=="2": add_subject()
        elif op=="3": add_note()
        elif op=="4": report_student(input("ID estudiante: ").strip())
        elif op=="5": export_all_reports()
        elif op=="0": break
        else: print("Inválido")

if __name__=="__main__":
    menu()


"""
Enunciado

Implementa un CLI para gestionar:

estudiantes.csv (student_id, name).

asignaturas.csv (subject_id, name, weight) — weight es ponderación de la asignatura en el promedio final.

notas.csv (note_id, student_id, subject_id, nota, tipo) — tipo puede ser PARCIAL, FINAL, TAREA.

Funcionalidades: registrar notas, calcular promedios por estudiante (ponderados por asignatura), determinar estado (APROBADO si promedio >= 3.5), exportar reporte por estudiante a CSV.

Validaciones: nota entre 0 y 5, ponderaciones suman 1.0 (o normalizar si no cumplen).

Código (completo y comentado)



"""