import csv
import os

USUARIOS_FILE = "usuarios.csv"
LIBROS_FILE = "libros.csv"


# ============================
# Cargar libros
# ============================
def cargar_libros():
    libros = {}
    if not os.path.exists(LIBROS_FILE):
        return libros
    
    with open(LIBROS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            libros[row["id_libro"]] = row["titulo"]
    return libros


# ============================
# Cargar usuarios
# ============================
def cargar_usuarios():
    usuarios = []
    if not os.path.exists(USUARIOS_FILE):
        return usuarios
    
    with open(USUARIOS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            libros_ids = row["libros"].split(",") if row["libros"] else []
            libros_ids = [x.strip() for x in libros_ids if x.strip() != ""]
            
            usuarios.append({
                "id": row["id_usuario"],
                "nombre": row["nombre"],
                "libros": libros_ids
            })
    return usuarios


# ============================
# Guardar usuarios
# ============================
def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id_usuario", "nombre", "libros"])
        
        for u in usuarios:
            writer.writerow([u["id"], u["nombre"], ",".join(u["libros"])])


# ============================
# Guardar libros
# ============================
def guardar_libros(libros):
    with open(LIBROS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id_libro", "titulo"])
        
        for id_libro, titulo in libros.items():
            writer.writerow([id_libro, titulo])


# ============================
# Mostrar usuarios con los libros que tienen
# ============================
def mostrar_usuarios(usuarios, libros):
    for usuario in usuarios:
        print(f"\nUsuario: {usuario['nombre']} (id {usuario['id']})")
        print("Libros que tiene:")

        if not usuario["libros"]:
            print("  - No tiene libros")
        else:
            for libro_id in usuario["libros"]:
                titulo = libros.get(libro_id, "Libro no encontrado")
                print(f"  - {titulo}")


# ============================
# Agregar usuario
# ============================
def agregar_usuario(usuarios):
    nuevo_id = str(len(usuarios) + 1)
    nombre = input("Nombre del usuario: ")
    
    usuarios.append({
        "id": nuevo_id,
        "nombre": nombre,
        "libros": []
    })
    
    guardar_usuarios(usuarios)
    print("Usuario agregado exitosamente.")


# ============================
# Agregar libro
# ============================
def agregar_libro(libros):
    nuevo_id = str(len(libros) + 1)
    titulo = input("Título del libro: ")
    
    libros[nuevo_id] = titulo
    guardar_libros(libros)
    
    print("Libro agregado correctamente.")


# ============================
# Asignar libro a usuario
# ============================
def asignar_libro(usuarios, libros):
    mostrar_usuarios(usuarios, libros)

    id_usuario = input("\nID del usuario: ")
    id_libro = input("ID del libro: ")

    for u in usuarios:
        if u["id"] == id_usuario:
            u["libros"].append(id_libro)
            guardar_usuarios(usuarios)
            print("Libro asignado exitosamente.")
            return
    
    print("Usuario no encontrado.")


# ============================
# Menú principal
# ============================
def menu():
    usuarios = cargar_usuarios()
    libros = cargar_libros()

    while True:
        print("\n===== MENÚ =====")
        print("1. Ver usuarios y sus libros")
        print("2. Agregar usuario")
        print("3. Agregar libro")
        print("4. Asignar libro a usuario")
        print("5. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            mostrar_usuarios(usuarios, libros)

        elif opcion == "2":
            agregar_usuario(usuarios)

        elif opcion == "3":
            agregar_libro(libros)

        elif opcion == "4":
            asignar_libro(usuarios, libros)

        elif opcion == "5":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")


# Ejecutar el menú
menu()
