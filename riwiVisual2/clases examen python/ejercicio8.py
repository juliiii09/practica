# sistema_inventario_auditoria.py
# Sistema completo: usuarios, equipos, prestamos y auditoría (CSV)
# Muy comentado para examen.
"""
Usuarios (crear, listar, cambiar rol).

Equipos (CRUD completo: crear, listar, buscar por id/nombre, editar, eliminar).

Préstamos (solicitar, aprobar, rechazar, devolver).

Auditoría: cada acción importante (crear usuario, crear equipo, aprobar, devolver) se registra en auditoria.csv con timestamp, usuario que realizó la acción y descripción.

Persistencia: usuarios.csv, equipos.csv, prestamos.csv, auditoria.csv.

Reglas: días por rol (TIEMPO_MAX). Validaciones de entrada y backups antes de sobrescribir.

Objetivos

Practicar CSV, backup, validaciones, modularidad, logs/auditoría y menús con submenús.

Debe ser tolerante a errores y fácil de usar en examen.

Pistas

Usa helpers leer_csv_dicts, escribir_csv_dicts, append_dict_en_csv.

Antes de cualquier write importante: crear backup.

Registrar auditoría en cada cambio que modifique los CSV.

Código (completo y comentado)

Guarda como sistema_inventario_auditoria.py.

"""




import csv, os, json
from datetime import datetime, timedelta
from shutil import copyfile

# --- Archivos y cabeceras ---
USERS_CSV = "si_usuarios.csv"
EQUIPOS_CSV = "si_equipos.csv"
PRESTAMOS_CSV = "si_prestamos.csv"
AUDITORIA_CSV = "si_auditoria.csv"

USERS_HEADER = ["usuario","contrasena","rol"]
EQUIPOS_HEADER = ["equipo_id","nombre_equipo","categoria","estado_actual","fecha_registro"]
PRESTAMOS_HEADER = ["prestamo_id","equipo_id","usuario_prestatario","tipo_usuario","fecha_solicitud","fecha_inicio","fecha_fin","dias","retraso","estado"]
AUDITORIA_HEADER = ["timestamp","actor","accion","detalle"]

# --- Reglas ---
TIEMPO_MAX = {"ESTUDIANTE":3, "INSTRUCTOR":7, "ADMINISTRATIVO":10}
MAX_LOGIN_INTENTOS = 3

# ---------------------
# Helpers (CSV/Backup/Auditoria)
# ---------------------
def asegurar_csv(path, header):
    """Crear CSV con cabecera si no existe."""
    if not os.path.exists(path):
        with open(path,"w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)

def leer_csv_dicts(path):
    """Leer CSV y devolver lista de diccionarios o [] si no existe."""
    if not os.path.exists(path):
        return []
    with open(path,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def escribir_csv_dicts(path, header, dicts):
    """Crear backup y sobrescribir CSV con lista de dicts."""
    if os.path.exists(path):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        copyfile(path, f"backup_{os.path.basename(path)}_{ts}")
    with open(path,"w",newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for d in dicts:
            writer.writerow(d)

def append_dict_en_csv(path, header, row):
    """Añadir fila a CSV; crear cabecera si no existe."""
    existe = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path,"a",newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if not existe:
            writer.writeheader()
        writer.writerow(row)

def auditar(actor, accion, detalle=""):
    """Escribe un registro en el CSV de auditoría con fecha/hora."""
    fila = {"timestamp": datetime.now().isoformat(), "actor": actor, "accion": accion, "detalle": detalle}
    append_dict_en_csv(AUDITORIA_CSV, AUDITORIA_HEADER, fila)

# ---------------------
# Usuario: CRUD mínimo y autenticación
# ---------------------
def crear_usuario(usuario, contrasena, rol="ADMIN"):
    usuarios = leer_csv_dicts(USERS_CSV)
    if any(u.get("usuario")==usuario for u in usuarios):
        return False
    fila = {"usuario":usuario, "contrasena":contrasena, "rol":rol}
    append_dict_en_csv(USERS_CSV, USERS_HEADER, fila)
    auditar("system", "crear_usuario", f"{usuario} rol={rol}")
    return True

def listar_usuarios():
    return leer_csv_dicts(USERS_CSV)

def cambiar_rol_usuario(usuario, nuevo_rol):
    usuarios = leer_csv_dicts(USERS_CSV)
    cambiado = False
    for u in usuarios:
        if u["usuario"] == usuario:
            u["rol"] = nuevo_rol
            cambiado = True
            break
    if cambiado:
        escribir_csv_dicts(USERS_CSV, USERS_HEADER, usuarios)
        auditar("system", "cambiar_rol", f"{usuario} -> {nuevo_rol}")
    return cambiado

def autenticar():
    usuarios = leer_csv_dicts(USERS_CSV)
    if not usuarios:
        print("No hay usuarios. Crea uno con usuario 'admin'/'admin'")
        crear_usuario("admin","admin","ADMIN")
        usuarios = leer_csv_dicts(USERS_CSV)
    intentos = 0
    while intentos < MAX_LOGIN_INTENTOS:
        u = input("Usuario: ").strip()
        p = input("Contraseña: ").strip()
        for row in usuarios:
            if row["usuario"] == u and row["contrasena"] == p:
                print("Login OK. Rol:", row["rol"])
                auditar(u, "login", "login correcto")
                return row
        intentos += 1
        print("Credenciales incorrectas. Intentos restantes:", MAX_LOGIN_INTENTOS - intentos)
    return None

# ---------------------
# Equipos: CRUD completo
# ---------------------
def generar_id_equipos(equipos):
    ids=[]
    for e in equipos:
        try:
            ids.append(int(e.get("equipo_id",0)))
        except: pass
    return str(max(ids)+1) if ids else "1"

def crear_equipo(nombre, categoria, actor="system"):
    equipos = leer_csv_dicts(EQUIPOS_CSV)
    nid = generar_id_equipos(equipos)
    fila = {"equipo_id":nid, "nombre_equipo":nombre, "categoria":categoria, "estado_actual":"DISPONIBLE", "fecha_registro": datetime.now().strftime("%Y-%m-%d")}
    append_dict_en_csv(EQUIPOS_CSV, EQUIPOS_HEADER, fila)
    auditar(actor, "crear_equipo", f"id={nid} nombre={nombre}")
    return fila

def listar_equipos():
    return leer_csv_dicts(EQUIPOS_CSV)

def buscar_equipo_por_id(eid):
    for e in leer_csv_dicts(EQUIPOS_CSV):
        if e["equipo_id"] == str(eid):
            return e
    return None

def buscar_equipos_por_nombre(texto):
    t = texto.lower()
    return [e for e in leer_csv_dicts(EQUIPOS_CSV) if t in e["nombre_equipo"].lower()]

def editar_equipo(eid, nombre=None, categoria=None, estado=None, actor="system"):
    equipos = leer_csv_dicts(EQUIPOS_CSV)
    cambiado=False
    for e in equipos:
        if e["equipo_id"] == str(eid):
            if nombre: e["nombre_equipo"]=nombre
            if categoria: e["categoria"]=categoria
            if estado: e["estado_actual"]=estado
            cambiado=True
            break
    if cambiado:
        escribir_csv_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, equipos)
        auditar(actor, "editar_equipo", f"id={eid}")
    return cambiado

def eliminar_equipo(eid, actor="system"):
    equipos = leer_csv_dicts(EQUIPOS_CSV)
    nuevos = [e for e in equipos if e["equipo_id"] != str(eid)]
    if len(nuevos) == len(equipos): return False
    escribir_csv_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, nuevos)
    auditar(actor, "eliminar_equipo", f"id={eid}")
    return True

# ---------------------
# Prestamos: CRUD y flujo (pendiente->aprobado->devuelto)
# ---------------------
def generar_id_prestamos(prestamos):
    ids=[]
    for p in prestamos:
        try: ids.append(int(p.get("prestamo_id",0)))
        except: pass
    return str(max(ids)+1) if ids else "1"

def crear_solicitud(equipo_id, usuario_prestatario, tipo_usuario, actor="system"):
    prestamos = leer_csv_dicts(PRESTAMOS_CSV)
    pid = generar_id_prestamos(prestamos)
    fila = {"prestamo_id": pid, "equipo_id": str(equipo_id), "usuario_prestatario": usuario_prestatario, "tipo_usuario": tipo_usuario.upper(),
            "fecha_solicitud": datetime.now().strftime("%Y-%m-%d"), "fecha_inicio":"", "fecha_fin":"", "dias":"", "retraso":"", "estado":"PENDIENTE"}
    append_dict_en_csv(PRESTAMOS_CSV, PRESTAMOS_HEADER, fila)
    auditar(actor, "crear_solicitud", f"id={pid} equipo={equipo_id} usuario={usuario_prestatario}")
    return fila

def listar_prestamos():
    return leer_csv_dicts(PRESTAMOS_CSV)

def listar_pendientes():
    return [p for p in leer_csv_dicts(PRESTAMOS_CSV) if p.get("estado","").upper()=="PENDIENTE"]

def aprobar_prestamo(pid, actor="system"):
    prestamos = leer_csv_dicts(PRESTAMOS_CSV)
    equipos = leer_csv_dicts(EQUIPOS_CSV)
    for p in prestamos:
        if p["prestamo_id"] == str(pid) and p["estado"].upper()=="PENDIENTE":
            # validar que equipo esté disponible
            equipo = next((e for e in equipos if e["equipo_id"]==p["equipo_id"]), None)
            if equipo and equipo.get("estado_actual","").upper() != "DISPONIBLE":
                return False, "Equipo no disponible"
            inicio = datetime.now().strftime("%Y-%m-%d")
            dias = TIEMPO_MAX.get(p.get("tipo_usuario","").upper(), 3)
            fin = (datetime.strptime(inicio,"%Y-%m-%d") + timedelta(days=dias)).strftime("%Y-%m-%d")
            p["fecha_inicio"]=inicio; p["fecha_fin"]=fin; p["dias"]=str(dias); p["estado"]="APROBADO"
            # marcar equipo prestado
            if equipo:
                equipo["estado_actual"]="PRESTADO"
                escribir_csv_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, equipos)
            escribir_csv_dicts(PRESTAMOS_CSV, PRESTAMOS_HEADER, prestamos)
            auditar(actor, "aprobar_prestamo", f"id={pid}")
            return True, "Aprobado"
    return False, "No encontrado o mal estado"

def registrar_devolucion(pid, actor="system"):
    prestamos = leer_csv_dicts(PRESTAMOS_CSV)
    equipos = leer_csv_dicts(EQUIPOS_CSV)
    for p in prestamos:
        if p["prestamo_id"] == str(pid) and p["estado"].upper()=="APROBADO":
            inicio = datetime.strptime(p["fecha_inicio"], "%Y-%m-%d")
            dias_usados = (datetime.now() - inicio).days
            max_dias = TIEMPO_MAX.get(p.get("tipo_usuario","").upper(), 3)
            retraso = max(0, dias_usados - max_dias)
            p["dias"]=str(dias_usados); p["retraso"]=str(retraso); p["fecha_fin"]=datetime.now().strftime("%Y-%m-%d"); p["estado"]="DEVUELTO"
            # marcar equipo disponible
            equipo = next((e for e in equipos if e["equipo_id"]==p["equipo_id"]), None)
            if equipo:
                equipo["estado_actual"]="DISPONIBLE"
                escribir_csv_dicts(EQUIPOS_CSV, EQUIPOS_HEADER, equipos)
            escribir_csv_dicts(PRESTAMOS_CSV, PRESTAMOS_HEADER, prestamos)
            auditar(actor, "devolucion", f"id={pid} retraso={retraso}")
            return True, "Devolución registrada"
    return False, "No encontrado o mal estado"

# ---------------------
# Menú principal (simple) - para examen
# ---------------------
def menu():
    # aseguramos archivos
    asegurar_csv(USERS_CSV, USERS_HEADER)
    asegurar_csv(EQUIPOS_CSV, EQUIPOS_HEADER)
    asegurar_csv(PRESTAMOS_CSV, PRESTAMOS_HEADER)
    asegurar_csv(AUDITORIA_CSV, AUDITORIA_HEADER)

    print("Inicia sesión para continuar:")
    user = autenticar()
    if not user:
        print("Login fallido. Saliendo.")
        return

    actor = user["usuario"]  # registro en auditoría
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1) Usuarios   2) Equipos   3) Préstamos   4) Auditoría   0) Salir")
        opt = input("Opción: ").strip()
        if opt == "1":
            # submenú usuarios (crear/listar/cambiar rol)
            print("\na) Crear usuario   b) Listar usuarios   c) Cambiar rol   v) Volver")
            o = input("op: ").strip().lower()
            if o == "a":
                u = input("usuario: ").strip(); p = input("contraseña: ").strip(); r = input("rol [ADMIN]: ").strip() or "ADMIN"
                ok = crear_usuario(u,p,r)
                print("Creado" if ok else "No creado (existe)")
            elif o == "b":
                for uu in listar_usuarios(): print(uu)
            elif o == "c":
                u = input("usuario a cambiar rol: ").strip(); nr = input("nuevo rol: ").strip()
                if cambiar_rol_usuario(u,nr):
                    print("Rol cambiado")
                else:
                    print("No existe usuario")
            else:
                continue

        elif opt == "2":
            print("\na) Crear equipo   b) Listar   c) Buscar por id   d) Buscar por nombre   e) Editar   f) Eliminar   v) Volver")
            o = input("op: ").strip().lower()
            if o == "a":
                n = input("nombre: ").strip(); c = input("categoria: ").strip()
                crear_equipo(n,c, actor)
                print("Creado")
            elif o == "b":
                for e in listar_equipos(): print(e)
            elif o == "c":
                eid = input("id: ").strip(); print(buscar_equipo_por_id(eid) or "No existe")
            elif o == "d":
                q = input("texto: ").strip(); res = buscar_equipos_por_nombre(q); [print(r) for r in res] or print("No coincide")
            elif o == "e":
                eid = input("id a editar: ").strip(); n = input("nuevo nombre (enter para mantener): ").strip() or None
                cat = input("nueva categoria (enter para mantener): ").strip() or None
                est = input("nuevo estado (enter para mantener): ").strip().upper() or None
                ok = editar_equipo(eid, n, cat, est, actor)
                print("Editado" if ok else "No se encontró")
            elif o == "f":
                eid = input("id a eliminar: ").strip()
                print("Eliminado" if eliminar_equipo(eid, actor) else "No existe")
            else:
                continue

        elif opt == "3":
            print("\na) Crear solicitud   b) Listar   c) Listar pendientes   d) Aprobar   e) Devolver   v) Volver")
            o = input("op: ").strip().lower()
            if o == "a":
                eq = input("id equipo: ").strip(); sol = input("nombre solicitante: ").strip(); tipo = input("tipo (Estudiante/Instructor/Administrativo): ").strip() or "ESTUDIANTE"
                crear_solicitud(eq, sol, tipo, actor)
                print("Solicitud creada")
            elif o == "b":
                for p in listar_prestamos(): print(p)
            elif o == "c":
                for p in listar_pendientes(): print(p)
            elif o == "d":
                pid = input("id a aprobar: ").strip()
                ok,msg = aprobar_prestamo(pid, actor)
                print(msg)
            elif o == "e":
                pid = input("id a devolver: ").strip()
                ok,msg = registrar_devolucion(pid, actor)
                print(msg)
            else:
                continue

        elif opt == "4":
            # mostrar auditoría (últimos 100)
            rows = leer_csv_dicts(AUDITORIA_CSV)
            for r in rows[-100:]:
                print(r)
        elif opt == "0":
            print("Saliendo..."); break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
