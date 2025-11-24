
"""
productos = []

for i in range(2):
    nombre = input("Ingresa el nombre del producto: ")
    precio = input("Ingresa el precio: ")

    producto = {
        "nombre": nombre,
        "precio": precio
    }

    productos.append(producto)

# Mostrar la lista
for p in productos:
    print("Producto:", p["nombre"], "— Precio:", p["precio"])
"""



    
# inventario_csv_simple.py
import csv
from datetime import datetime

CSV_FILE = "inventario.csv"

def guardar_en_csv(lista_productos):
    """Sobrescribe inventario.csv con la lista de productos."""
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # cabecera
        writer.writerow(["id", "nombre", "cantidad", "fecha_registro"])
        for p in lista_productos:
            writer.writerow([p["id"], p["nombre"], p["cantidad"], p["fecha_registro"]])

def leer_desde_csv():
    """Lee inventario.csv y devuelve lista de diccionarios."""
    productos = []
    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            # leer cabecera (y evitar tratarla como dato)
            try:
                next(reader)
            except StopIteration:
                return productos
            for row in reader:
                if len(row) >= 3:
                    productos.append({
                        "id": int(row[0]),
                        "nombre": row[1],
                        "cantidad": int(row[2]),
                        # si hay fecha en la fila la usamos, si no, ponemos ""
                        "fecha_registro": row[3] if len(row) > 3 else ""
                    })
    except FileNotFoundError:
        # si no existe el archivo, devolvemos lista vacía
        return []
    return productos

def pedir_int(mensaje):
    """Pide un entero hasta que el usuario introduzca uno válido."""
    while True:
        valor = input(mensaje).strip()
        try:
            return int(valor)
        except ValueError:
            print("Por favor escribe un número entero.")

def main():
    print("=== REGISTRAR 3 PRODUCTOS (se guardarán en inventario.csv) ===")
    productos = []

    for i in range(3):
        print(f"\nProducto {i+1}:")
        pid = pedir_int("ID (número): ")
        nombre = input("Nombre: ").strip()
        cantidad = pedir_int("Cantidad (número): ")

        producto = {
            "id": pid,
            "nombre": nombre,
            "cantidad": cantidad,
            "fecha_registro": datetime.now().strftime("%Y-%m-%d")
        }
        productos.append(producto)

    # Guardar lo ingresado en CSV
    guardar_en_csv(productos)
    print(f"\nSe guardaron {len(productos)} productos en '{CSV_FILE}'.")

    # Leer el CSV y mostrar inventario
    print("\n=== Inventario actual (leer desde CSV) ===")
    inventario = leer_desde_csv()
    for p in inventario:
        print(p)

    # Buscar por ID y actualizar cantidad
    print("\n=== Buscar producto para actualizar cantidad ===")
    buscar_id = pedir_int("Ingresa el ID a buscar: ")
    encontrado = None
    for p in inventario:
        if p["id"] == buscar_id:
            encontrado = p
            break

    if encontrado:
        print("Producto encontrado:", encontrado)
        nueva = pedir_int("Nueva cantidad: ")
        encontrado["cantidad"] = nueva
        # guardar cambios en CSV
        guardar_en_csv(inventario)
        print("Cantidad actualizada y CSV guardado.")
        print("\nInventario actualizado:")
        for p in inventario:
            print(p)
    else:
        print("Producto no encontrado. No se hicieron cambios.")

if __name__ == "__main__":
    main()

"""

-----estructura mas simple de csv


import csv

# Abrimos el archivo CSV en modo escritura
with open("productos.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # 1. Escribimos la CABECERA (nombres de las columnas)
    writer.writerow(["id", "nombre", "cantidad"])

    # 2. Escribimos DOS PRODUCTOS
    writer.writerow([1, "Pan", 10])
    writer.writerow([2, "Leche", 20])

print("Archivo CSV creado!")


"""