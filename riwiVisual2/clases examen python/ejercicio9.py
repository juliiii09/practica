# biblioteca_reservas_multas.py
# Sistema de biblioteca con control de copias, multas y reportes

import csv, os, json
from datetime import datetime, timedelta
from shutil import copyfile

BOOKS_CSV = "libros.csv"
USERS_CSV = "bibl_usuarios.csv"
LOANS_CSV = "bibl_prestamos.csv"

BOOKS_HEADER = ["book_id","title","author","copies_total","copies_available"]
USERS_HEADER = ["user_id","name","rol"]
LOANS_HEADER = ["loan_id","book_id","user_id","date_start","date_due","date_returned","dias_usados","multa","estado"]

# reglas
DAYS_DEFAULT = 14
FEE_PER_DAY = {"ESTUDIANTE":200, "PROFESOR":0, "ADMIN":0}

def asegurar(path, header):
    if not os.path.exists(path):
        with open(path,"w",newline="",encoding="utf-8") as f:
            csv.writer(f).writerow(header)

def read(path):
    if not os.path.exists(path): return []
    with open(path,newline="",encoding="utf-8") as f: return list(csv.DictReader(f))

def write(path, header, rows):
    # backup
    if os.path.exists(path):
        copyfile(path, path + ".bak")
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
        try: ids.append(int(r[key]))
        except: pass
    return str(max(ids)+1) if ids else "1"

# Funciones de libros
def add_book():
    books = read(BOOKS_CSV)
    bid = next_id(books, "book_id")
    t = input("Título: ").strip(); a = input("Autor: ").strip()
    copies = int(input("Cantidad total de copias: ").strip() or "1")
    row = {"book_id":bid,"title":t,"author":a,"copies_total":str(copies),"copies_available":str(copies)}
    append(BOOKS_CSV, BOOKS_HEADER, row)
    print("Libro agregado:", row)

def list_books():
    for b in read(BOOKS_CSV): print(b)

# Usuarios
def add_user():
    users = read(USERS_CSV)
    uid = next_id(users, "user_id")
    n = input("Nombre: ").strip(); rol = input("Rol (ESTUDIANTE/PROFESOR): ").strip().upper() or "ESTUDIANTE"
    append(USERS_CSV, USERS_HEADER, {"user_id":uid,"name":n,"rol":rol}); print("Usuario creado")

def list_users():
    for u in read(USERS_CSV): print(u)

# Prestamos
def loan_book():
    books = read(BOOKS_CSV); users = read(USERS_CSV); loans = read(LOANS_CSV)
    bid = input("Book ID: ").strip()
    book = next((b for b in books if b["book_id"]==bid), None)
    if not book: print("Libro no existe"); return
    if int(book["copies_available"]) <= 0: print("No hay copias disponibles"); return
    uid = input("User ID: ").strip()
    user = next((u for u in users if u["user_id"]==uid), None)
    if not user: print("Usuario no existe"); return
    loan_id = next_id(loans,"loan_id")
    start = datetime.now().strftime("%Y-%m-%d")
    due = (datetime.now() + timedelta(days=DAYS_DEFAULT)).strftime("%Y-%m-%d")
    row = {"loan_id":loan_id,"book_id":bid,"user_id":uid,"date_start":start,"date_due":due,"date_returned":"","dias_usados":"","multa":"0","estado":"APROBADO"}
    append(LOANS_CSV, LOANS_HEADER, row)
    # actualizar copia disponible
    for b in books:
        if b["book_id"]==bid:
            b["copies_available"] = str(int(b["copies_available"]) - 1)
    write(BOOKS_CSV, BOOKS_HEADER, books)
    print("Prestamo creado:", row)

def return_book():
    loans = read(LOANS_CSV); books = read(BOOKS_CSV); users = read(USERS_CSV)
    lid = input("Loan ID a devolver: ").strip()
    for l in loans:
        if l["loan_id"]==lid and l["estado"]=="APROBADO":
            start = datetime.strptime(l["date_start"], "%Y-%m-%d")
            dias = (datetime.now() - start).days
            user = next((u for u in users if u["user_id"]==l["user_id"]), None)
            rol = user["rol"] if user else "ESTUDIANTE"
            multa = max(0, dias - DAYS_DEFAULT) * FEE_PER_DAY.get(rol, 200)
            l["date_returned"] = datetime.now().strftime("%Y-%m-%d")
            l["dias_usados"] = str(dias)
            l["multa"] = str(multa)
            l["estado"] = "DEVUELTO"
            # liberar copia
            for b in books:
                if b["book_id"]==l["book_id"]:
                    b["copies_available"] = str(int(b["copies_available"]) + 1)
            write(BOOKS_CSV, BOOKS_HEADER, books)
            write(LOANS_CSV, LOANS_HEADER, loans)
            print("Devolución procesada. Multa:", multa)
            return
    print("Loan ID inválido o no está en estado APROBADO")

# Reportes
def reporte_top_libros():
    loans = read(LOANS_CSV)
    counts = {}
    for l in loans:
        bid = l["book_id"]
        counts[bid] = counts.get(bid,0) + 1
    # ordenar desc
    orden = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    for bid, cnt in orden[:10]:
        book = next((b for b in read(BOOKS_CSV) if b["book_id"]==bid), None)
        print(book["title"] if book else bid, cnt)

def export_loans_json():
    loans = read(LOANS_CSV)
    with open("loans_report.json","w",encoding="utf-8") as f: json.dump(loans,f,ensure_ascii=False, indent=2)
    print("Exportado loans_report.json")

# Menu
def menu():
    asegurar(BOOKS_CSV, BOOKS_HEADER); asegurar(USERS_CSV, USERS_HEADER); asegurar(LOANS_CSV, LOANS_HEADER)
    while True:
        print("\\n--- BIBLIOTECA ---")
        print("1) Agregar libro   2) Listar libros   3) Agregar usuario   4) Listar usuarios")
        print("5) Prestar libro   6) Devolver libro   7) Top libros   8) Exportar prestamos JSON   0) Salir")
        op = input("Opción: ").strip()
        if op=="1": add_book()
        elif op=="2": list_books()
        elif op=="3": add_user()
        elif op=="4": list_users()
        elif op=="5": loan_book()
        elif op=="6": return_book()
        elif op=="7": reporte_top_libros()
        elif op=="8": export_loans_json()
        elif op=="0": break
        else: print("Inválido")

if __name__=="__main__":
    menu()

"""
Enunciado

Implementa un sistema para gestionar libros, préstamos y multas:

libros.csv (book_id, title, author, copies_total, copies_available).

usuarios.csv (user_id, name, rol).

prestamos_libros.csv (loan_id, book_id, user_id, date_start, date_due, date_returned, dias_usados, multa, estado).

Reglas: préstamo básico 14 días; multa por día de retraso: tarifa variable por tipo de usuario (ej. ESTUDIANTE=200, PROFESOR=0).

Funcionalidades: crear libros/usuarios, prestar libro (disminuye copies_available), devolver (calcular multa), reportes (libros más prestados, usuarios con mayor multa), exportar CSV->JSON.

Código (completo y comentado)

Guarda como biblioteca_reservas_multas.py.

"""