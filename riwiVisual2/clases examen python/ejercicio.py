# no_math_crud.py
# CRUD simple para contactos (nombre + email)

CONTACTS_FILE = "contacts.csv"
FIELDS = ["id","name","email"]

import csv, os

def asegurar():
    if not os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE,"w",newline="",encoding="utf-8") as f:
            csv.writer(f).writerow(FIELDS)

def leer():
    if not os.path.exists(CONTACTS_FILE): return []
    with open(CONTACTS_FILE,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def escribir(lista):
    with open(CONTACTS_FILE,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
        for l in lista: w.writerow(l)

def add():
    lista = leer()
    nid = str(max([int(x["id"]) for x in lista])+1) if lista else "1"
    name = input("Nombre: ").strip()
    email = input("Email: ").strip()
    lista.append({"id":nid,"name":name,"email":email})
    escribir(lista); print("Agregado")

def show():
    for r in leer(): print(r)

def find():
    q = input("Buscar por nombre o id: ").strip().lower()
    res = [r for r in leer() if r["id"]==q or q in r["name"].lower()]
    if not res: print("No encontrado")
    else: [print(x) for x in res]

def update():
    lista = leer(); idb = input("ID a actualizar: ").strip()
    for r in lista:
        if r["id"]==idb:
            nr = input(f"Nuevo nombre ({r['name']}): ").strip() or r["name"]
            ne = input(f"Nuevo email ({r['email']}): ").strip() or r["email"]
            r["name"]=nr; r["email"]=ne
            escribir(lista); print("Actualizado"); return
    print("No existe")

def delete():
    lista = leer(); idb = input("ID a eliminar: ").strip()
    n = [x for x in lista if x["id"]!=idb]
    if len(n)==len(lista): print("No existe")
    else: escribir(n); print("Eliminado")

def menu():
    asegurar()
    while True:
        print("\n--- CONTACTS CRUD ---")
        print("1 Add 2 Show 3 Find 4 Update 5 Delete 0 Exit")
        o = input("Opción: ").strip()
        if o=="1": add()
        elif o=="2": show()
        elif o=="3": find()
        elif o=="4": update()
        elif o=="5": delete()
        elif o=="0": break
        else: print("Inválido")

if __name__=="__main__":
    menu()
