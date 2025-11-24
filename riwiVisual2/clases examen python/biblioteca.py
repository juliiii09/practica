# library_manager.py
import csv, json, os
from datetime import datetime

BOOKS_CSV = "books.csv"
BOOKS_JSON = "books.json"
BOOKS_HEADER = ["book_id","title","author","year","available"]

def asegurar_csv(path, header):
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f); writer.writerow(header)

def leer_books():
    if not os.path.exists(BOOKS_CSV): return []
    with open(BOOKS_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def escribir_books(books):
    with open(BOOKS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=BOOKS_HEADER); writer.writeheader()
        for b in books: writer.writerow(b)

def append_book(book):
    existe = os.path.exists(BOOKS_CSV) and os.path.getsize(BOOKS_CSV)>0
    with open(BOOKS_CSV,"a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=BOOKS_HEADER)
        if not existe: w.writeheader()
        w.writerow(book)

def next_id(books):
    ids = []
    for b in books:
        try: ids.append(int(b["book_id"]))
        except: pass
    return str(max(ids)+1) if ids else "1"

def add_book():
    books = leer_books()
    bid = next_id(books)
    title = input("Título: ").strip()
    author = input("Autor: ").strip()
    year = input("Año: ").strip()
    book = {"book_id": bid, "title": title, "author": author, "year": year, "available": "True"}
    append_book(book)
    print("Libro añadido:", book)

def list_books():
    for b in leer_books(): print(b)

def find_book():
    q = input("ID o título (parte): ").strip().lower()
    found = [b for b in leer_books() if b["book_id"]==q or q in b["title"].lower()]
    if not found: print("No encontrado")
    else:
        for b in found: print(b)

def edit_book():
    books = leer_books()
    bid = input("ID a editar: ").strip()
    for b in books:
        if b["book_id"] == bid:
            t = input(f"Título ({b['title']}): ").strip() or b['title']
            a = input(f"Autor ({b['author']}): ").strip() or b['author']
            y = input(f"Año ({b['year']}): ").strip() or b['year']
            b.update({"title":t,"author":a,"year":y})
            escribir_books(books); print("Editado"); return
    print("ID no encontrado")

def delete_book():
    books = leer_books()
    bid = input("ID a eliminar: ").strip()
    new = [b for b in books if b["book_id"]!=bid]
    if len(new)==len(books): print("No encontrado")
    else:
        escribir_books(new); print("Eliminado")

def export_json():
    books = leer_books()
    with open(BOOKS_JSON,"w",encoding="utf-8") as f: json.dump(books,f,ensure_ascii=False, indent=2)
    print("Exportado a JSON")

def import_json():
    if not os.path.exists(BOOKS_JSON): print("No hay JSON"); return
    with open(BOOKS_JSON,"r",encoding="utf-8") as f: data = json.load(f)
    escribir_books(data); print("Importado JSON a CSV")

def menu():
    asegurar_csv(BOOKS_CSV, BOOKS_HEADER)
    while True:
        print("\\n1) Añadir 2) Listar 3) Buscar 4) Editar 5) Eliminar 6) Exportar JSON 7) Importar JSON 0) Salir")
        o = input("Opción: ").strip()
        if o=="1": add_book()
        elif o=="2": list_books()
        elif o=="3": find_book()
        elif o=="4": edit_book()
        elif o=="5": delete_book()
        elif o=="6": export_json()
        elif o=="7": import_json()
        elif o=="0": break
        else: print("Inválido")

if __name__=="__main__": menu()
