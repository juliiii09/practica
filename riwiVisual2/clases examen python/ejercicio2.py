# loops_conditions_validations.py
# Ejemplos y mini-CRUD que usa ciclos anidados y validaciones fuertes

def pedir_entero(prompt, minimo=None, maximo=None):
    while True:
        s = input(prompt).strip()
        try:
            n = int(s)
            if minimo is not None and n < minimo:
                print("Debe ser >= ", minimo); continue
            if maximo is not None and n > maximo:
                print("Debe ser <= ", maximo); continue
            return n
        except:
            print("Escribe un entero válido.")

# ejemplo de ciclo anidado: matriz y búsqueda
def matriz_demo():
    filas = pedir_entero("Filas matriz (ej:3): ", 1)
    cols = pedir_entero("Columnas matriz (ej:3): ", 1)
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(cols):
            v = pedir_entero(f"Valor [{i},{j}]: ")
            fila.append(v)
        matriz.append(fila)
    print("Matriz ingresada:")
    for fila in matriz:
        print(fila)
    # busqueda de un valor
    objetivo = pedir_entero("Valor a buscar en matriz: ")
    encontrados = []
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == objetivo:
                encontrados.append((i,j))
    print("Posiciones encontradas:", encontrados)

# ejemplo acumulador + condicionales
def stats_demo():
    n = pedir_entero("¿Cuántos números vas a ingresar?: ", 1)
    suma = 0
    pares = 0
    impares = 0
    mayores5 = 0
    for i in range(n):
        v = pedir_entero(f"número {i+1}: ")
        suma += v
        if v % 2 == 0: pares += 1
        else: impares += 1
        if v > 5: mayores5 += 1
    print("Suma:", suma, "Promedio:", suma/n, "Pares:", pares, "Impares:", impares, "Mayores5:", mayores5)

# ejemplo validación de texto y búsqueda en lista de dicts
def people_demo():
    lista = []
    while True:
        name = input("Nombre (enter para salir): ").strip()
        if not name: break
        age = pedir_entero("Edad: ", 0)
        tags = input("Tags (separados por coma) o enter: ").strip()
        tags_list = [t.strip() for t in tags.split(",")] if tags else []
        lista.append({"name":name,"age":age,"tags":tags_list})
    print("Personas guardadas:", lista)
    
    
    # buscar por tag con ciclo anidado
    tag = input("Buscar personas por tag (enter para omitir): ").strip()
    if tag:
        for p in lista:
            for t in p["tags"]:
                if t.lower() == tag.lower():
                    print("Coincide:", p)
                    break

def menu():
    while True:
        print("\n--- LOOPS / CONDITIONS / VALIDATIONS ---")
        print("1 Matriz demo 2 Stats demo 3 People demo 0 Salir")
        o = input("Opción: ").strip()
        if o=="1": matriz_demo()
        elif o=="2": stats_demo()
        elif o=="3": people_demo()
        elif o=="0": break
        else: print("Inválido")

if __name__=="__main__":
    menu()
    
    
    
    
    
    
    
    
    
    
    
    
    #prestamo de libros

"""
import json, os

FILE = "libros.json"


def asegurar():
    if not os.path.exists(FILE):
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def leer():
    with open(FILE, encoding="utf-8") as f:
        return json.load(f)


def escribir(lista):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)


def crear():
    lista = leer()
    libro = {
        "titulo": input("Título: "),
        "autor": input("Autor: "),
        "año": input("Año: "),
        "categoria": input("Categoría: ")
    }
    lista.append(libro)
    escribir(lista)
    print("Creado.\n")


def listar():
    for l in leer(): print(l)
    print()


def buscar():
    q = input("Texto a buscar: ").lower()
    for l in leer():
        if q in l["titulo"].lower():
            print("Encontrado:", l)


def menu():
    asegurar()
    while True:
        print("1 Crear 2 Listar 3 Buscar 0 Salir")
        op = input("Opción: ")

        if op == "1": crear()
        elif op == "2": listar()
        elif op == "3": buscar()
        elif op == "0": break


menu()





"""




"""


EJERCICIO 4 – CSV + validaciones + fechas
Enunciado

Crea un sistema para registrar préstamos de libros:

Cada préstamo tiene:

id

libro

usuario

fecha préstamo

fecha devolución

días usados

retraso (si > 7 días)

Debe permitir:

Registrar préstamo

Registrar devolución

Listar todo

Solución simplificada
import csv, os
from datetime import datetime, timedelta

FILE = "prestamos.csv"
HEAD = ["id", "libro", "usuario", "fecha_prestamo", "fecha_devolucion", "dias", "retraso"]


def asegurar():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(HEAD)


def leer():
    with open(FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def escribir(lista):
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEAD)
        w.writeheader()
        for r in lista:
            w.writerow(r)


def next_id(lista):
    return str(max([int(x["id"]) for x in lista], default=0) + 1)


def prestar():
    lista = leer()
    now = datetime.now().strftime("%Y-%m-%d")

    nuevo = {
        "id": next_id(lista),
        "libro": input("Libro: "),
        "usuario": input("Usuario: "),
        "fecha_prestamo": now,
        "fecha_devolucion": "",
        "dias": "",
        "retraso": ""
    }

    lista.append(nuevo)
    escribir(lista)
    print("Prestamo registrado.\n")


def devolver():
    lista = leer()
    idb = input("ID préstamo: ")

    for p in lista:
        if p["id"] == idb:
            inicio = datetime.strptime(p["fecha_prestamo"], "%Y-%m-%d")
            fin = datetime.now()
            dias = (fin - inicio).days
            retraso = max(0, dias - 7)

            p["fecha_devolucion"] = fin.strftime("%Y-%m-%d")
            p["dias"] = dias
            p["retraso"] = retraso

            escribir(lista)
            print("Devuelto.\n")
            return

    print("No existe.\n")


def listar():
    for p in leer(): print(p)
    print()


def menu():
    asegurar()
    while True:
        print("1 Prestar\n2 Devolver\n3 Listar\n0 Salir")
        op = input("Opción: ")

        if op == "1": prestar()
        elif op == "2": devolver()
        elif op == "3": listar()
        elif op == "0": break


menu()



"""




"""




"""

