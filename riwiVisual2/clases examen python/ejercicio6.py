# backup_restore.py
import os
from shutil import copyfile
from datetime import datetime

def crear_backup(path):
    if not os.path.exists(path):
        print("Archivo no existe:", path); return None
    base = os.path.basename(path)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = f"backup_{base}_{ts}"
    copyfile(path, dest)
    print("Backup creado:", dest)
    return dest

def listar_backups():
    # lista archivos que empiezan con 'backup_'
    items = [f for f in os.listdir(".") if f.startswith("backup_")]
    for i, it in enumerate(items):
        print(i, it)
    return items

def restaurar_backup(indice):
    items = listar_backups()
    try:
        sel = items[int(indice)]
    except:
        print("Índice inválido"); return
    # asume que el nombre sigue formato backup_<original>_timestamp
    parts = sel.split("_")
    original = "_".join(parts[1:-1])  # reconstruye el nombre original
    # si original no existe en cwd, preguntar nombre destino
    destino = input(f"Restaurar {sel} a (enter para sobrescribir {original}): ").strip() or original
    copyfile(sel, destino)
    print("Restaurado a", destino)

def menu():
    while True:
        print("\n--- BACKUP / RESTORE ---")
        print("1) Crear backup de archivo")
        print("2) Listar backups")
        print("3) Restaurar por índice")
        print("0) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            path = input("Ruta del archivo a respaldar: ").strip()
            crear_backup(path)
        elif op == "2":
            listar_backups()
        elif op == "3":
            idx = input("Indice backup: ").strip()
            restaurar_backup(idx)
        elif op == "0":
            break
        else:
            print("Inválido")

if __name__ == "__main__":
    menu()
