"""

CRUD significa:

Letra	Acción	Significado
C	Create	Crear un nuevo registro (agregar)
R	Read	Leer o mostrar registros
U	Update	Actualizar un registro existente
D	Delete	Eliminar un registro

Se puede aplicar a:

listas

diccionarios

archivos CSV

JSON

bases de datos
"""

"""
# CRUD MUY SENCILLO
# Lista donde vamos a guardar nombres (strings)
personas = []

def crear():
    # C = Create
    nombre = input("Ingresa un nombre: ")
    personas.append(nombre)
    print("✔ Persona agregada.")

def leer():
    # R = Read
    print("\n📌 Lista de personas:")
    for p in personas:
        print("-", p)

def actualizar():
    # U = Update
    viejo = input("Nombre que quieres modificar: ")
    if viejo in personas:
        nuevo = input("Nuevo nombre: ")
        # reemplazar usando índice
        indice = personas.index(viejo)
        personas[indice] = nuevo
        print("✔ Actualizado.")
    else:
        print("❌ No encontrado.")

def eliminar():
    # D = Delete
    nombre = input("Nombre a eliminar: ")
    if nombre in personas:
        personas.remove(nombre)
        print("✔ Eliminado.")
    else:
        print("❌ No encontrado.")

def menu():
    while True:
        print("\n--- CRUD BÁSICO ---")
        print("1. Crear")
        print("2. Leer")
        print("3. Actualizar")
        print("4. Eliminar")
        print("0. Salir")

        op = input("Opción: ")

        if op == "1": crear()
        elif op == "2": leer()
        elif op == "3": actualizar()
        elif op == "4": eliminar()
        elif op == "0":
            print("Adiós")
            break
        else:
            print("Opción inválida.")

menu()

"""


"""
# CRUD de personas usando diccionarios
# Cada persona tiene un id, nombre y edad

personas = []  # lista de diccionarios

def generar_id():
    # Genera ID consecutivo basado en la cantidad de registros
    return len(personas) + 1

def crear():
    nombre = input("Nombre: ")
    edad = input("Edad: ")

    persona = {
        "id": generar_id(),
        "nombre": nombre,
        "edad": edad
    }

    personas.append(persona)
    print("✔ Persona registrada.")

def leer():
    print("\n📌 LISTA DE PERSONAS:")
    for p in personas:
        print(f"ID: {p['id']} | Nombre: {p['nombre']} | Edad: {p['edad']}")

def buscar_por_id():
    id_buscar = int(input("ID a buscar: "))
    for p in personas:
        if p["id"] == id_buscar:
            print("Encontrado:", p)
            return p
    print("❌ No existe.")
    return None

def actualizar():
    persona = buscar_por_id()
    if persona:
        print("Deja vacío si no quieres cambiar un dato.")
        nuevo_nombre = input("Nuevo nombre: ")
        nueva_edad = input("Nueva edad: ")

        if nuevo_nombre:
            persona["nombre"] = nuevo_nombre
        if nueva_edad:
            persona["edad"] = nueva_edad

        print("✔ Actualizado.")

def eliminar():
    persona = buscar_por_id()
    if persona:
        personas.remove(persona)
        print("✔ Eliminado.")

def menu():
    while True:
        print("\n--- CRUD Personas (Nivel Medio) ---")
        print("1. Crear persona")
        print("2. Mostrar todas")
        print("3. Actualizar persona")
        print("4. Eliminar persona")
        print("0. Salir")
        op = input("Opción: ")

        if op == "1": crear()
        elif op == "2": leer()
        elif op == "3": actualizar()
        elif op == "4": eliminar()
        elif op == "0": break
        else: print("Inválido")

menu()
"""

import csv
import os

ARCHIVO = "inventario.csv"
CAMPOS = ["id", "nombre", "cantidad"]

def asegurar_archivo():
    """Crea el CSV si no existe."""
    if not os.path.exists(ARCHIVO):
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CAMPOS)  # cabeceras

def leer_todo():
    """Lee todo el archivo CSV y retorna lista de dicts."""
    with open(ARCHIVO, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def escribir_todo(lista):
    """Sobrescribe el archivo con la nueva lista."""
    with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        writer.writeheader()
        for item in lista:
            writer.writerow(item)

def generar_id(lista):
    """Genera un ID numérico basado en los existentes."""
    ids = [int(i["id"]) for i in lista]
    return str(max(ids) + 1) if ids else "1"

# -------------------
#   CRUD
# -------------------

def crear():
    lista = leer_todo()
    nuevo_id = generar_id(lista)
    nombre = input("Nombre producto: ")
    cantidad = int(input("Cantidad: "))

    fila = {"id": nuevo_id, "nombre": nombre, "cantidad": cantidad}
    lista.append(fila)

    escribir_todo(lista)
    print("✔ Registrado")

def leer():
    lista = leer_todo()
    print("\n📦 INVENTARIO:")
    for item in lista:
        print(f"ID: {item['id']} | Nombre: {item['nombre']} | Cantidad: {item['cantidad']}")

def buscar_por_id():
    lista = leer_todo()
    id_b = input("ID: ")

    for item in lista:
        if item["id"] == id_b:
            return item
    return None


def actualizar():
    lista = leer_todo()          # leemos UNA vez y trabajamos sobre esa lista
    id_b = input("ID a actualizar: ").strip()

    # buscamos el elemento dentro de la misma lista 'lista'
    encontrado = None
    for item in lista:
        if item["id"] == id_b:
            encontrado = item
            break

    if encontrado:
        print("Dejar vacío si no deseas cambiarlo.")
        nuevo_nombre = input("Nuevo nombre: ").strip()
        nueva_cant = input("Nueva cantidad: ").strip()

        if nuevo_nombre:
            encontrado["nombre"] = nuevo_nombre
        if nueva_cant:
            encontrado["cantidad"] = nueva_cant

        escribir_todo(lista)   # sobrescribimos la lista modificada
        print("✔ Actualizado")
    else:
        print("❌ No encontrado")


def eliminar():
    lista = leer_todo()
    id_b = input("ID a eliminar: ")
    nueva_lista = [item for item in lista if item["id"] != id_b]

    if len(nueva_lista) == len(lista):
        print("❌ No existe ese ID")
    else:
        escribir_todo(nueva_lista)
        print("✔ Eliminado")

def menu():
    asegurar_archivo()
    while True:
        print("\n--- CRUD Inventario CSV ---")
        print("1. Crear")
        print("2. Leer")
        print("3. Actualizar")
        print("4. Eliminar")
        print("0. Salir")
        op = input("Opción: ")

        if op == "1": crear()
        elif op == "2": leer()
        elif op == "3": actualizar()
        elif op == "4": eliminar()
        elif op == "0": break
        else:
            print("Inválido")

menu()
