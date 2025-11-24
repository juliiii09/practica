"""
TechLab CLI Project - single-file educational implementation

Archivo: techlab_cli_project.py
Referencia del enunciado subido: /mnt/data/Prueba_Desempeno_TechLab (1).docx

Este archivo contiene:
- Clases organizadas para un sistema de inventario y préstamos (Users, Equipment, Loans)
- Helpers para CSV y JSON
- Múltiples funciones y verificaciones (CRUD) para equipos y préstamos
- Menú de consola con opciones: gestión de usuarios, equipos, préstamos, reportes
- Ejemplos de uso, comentarios y notas de lógica para el examen

Cómo usar:
- Abre este archivo en VS Code o tu editor preferido.
- Ejecuta: python techlab_cli_project.py
- El sistema crea/usa los CSV: usuarios.csv, equipos.csv, prestamos.csv

Nota rápida: el objetivo es pedagógico: código claro, extensible y con muchas funciones
para poder consultarlo durante el examen.

"""

import csv
import json
import os
from datetime import datetime, timedelta
from getpass import getpass

# -----------------------------
# Configuración de archivos
# -----------------------------
USERS_CSV = "usuarios.csv"
EQUIPOS_CSV = "equipos.csv"
PRESTAMOS_CSV = "prestamos.csv"

# Cabeceras que se usarán en los CSV
USERS_HEADER = ["usuario", "contrasena", "rol"]
EQUIPOS_HEADER = ["equipo_id", "nombre_equipo", "categoria", "estado_actual", "fecha_registro"]
PRESTAMOS_HEADER = ["prestamo_id","equipo_id","nombre_equipo","usuario_prestatario","tipo_usuario","fecha_solicitud","fecha_inicio","fecha_fin","dias","retraso","estado","mes","anio"]

# Reglas del sistema (config)
TIEMPO_MAX = {"ESTUDIANTE":3, "INSTRUCTOR":7, "ADMINISTRATIVO":10}
MAX_LOGIN_INTENTOS = 3

# -----------------------------
# Helpers CSV / JSON / Fechas
# -----------------------------

def asegurar_csv(path, header):
    """Crea el CSV con cabecera si no existe."""
    if not os.path.exists(path):
        with open(path, mode="w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)


def leer_csv_como_dicts(path):
    """Lee CSV y devuelve lista de diccionarios. Si no existe devuelve []."""
    if not os.path.exists(path):
        return []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def escribir_dicts_en_csv(path, fieldnames, dicts):
    """Sobrescribe CSV con lista de dicts y cabecera fieldnames."""
    with open(path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for d in dicts:
            writer.writerow(d)


def append_dict_en_csv(path, fieldnames, dict_row):
    """Añade una fila al CSV, creando cabecera si hace falta."""
    existe = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not existe:
            writer.writeheader()
        writer.writerow(dict_row)


def leer_json(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def escribir_json(path, obj):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def hoy_str():
    return datetime.now().strftime('%Y-%m-%d')


def sumar_dias(fecha_str, dias):
    d = datetime.strptime(fecha_str, '%Y-%m-%d')
    return (d + timedelta(days=dias)).strftime('%Y-%m-%d')


def dias_entre(fecha_inicio_str, fecha_fin_str=None):
    inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
    fin = datetime.now() if fecha_fin_str is None else datetime.strptime(fecha_fin_str, '%Y-%m-%d')
    return (fin - inicio).days

# -----------------------------
# Funciones de validación y utilidades de consola
# -----------------------------

def pedir_entero(prompt):
    while True:
        v = input(prompt).strip()
        try:
            return int(v)
        except ValueError:
            print('Escribe un número entero válido.')


def pedir_entero_positivo(prompt):
    while True:
        n = pedir_entero(prompt)
        if n >= 0:
            return n
        print('Escribe un entero >= 0.')


def pedir_str_no_vacio(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print('No puede quedar vacío.')

# -----------------------------
# Clases para organizar lógica (Users, Equipment, Loans)
# -----------------------------

class UserManager:
    """Gestión simple de usuarios: carga, verificación y creación.

    Métricas añadidas:
    - listar usuarios
    - cambiar contraseña
    - eliminar usuario
    - crear usuario desde menú
    """
    def __init__(self, path=USERS_CSV):
        self.path = path
        asegurar_csv(self.path, USERS_HEADER)

    def cargar(self):
        return leer_csv_como_dicts(self.path)

    def escribir_todos(self, usuarios):
        """Sobrescribe el CSV de usuarios con la lista de diccionarios dada."""
        escribir_dicts_en_csv(self.path, USERS_HEADER, usuarios)

    def crear(self, usuario, contrasena, rol='ADMIN'):
        usuarios = self.cargar()
        # evitar duplicados por 'usuario'
        if any(u.get('usuario') == usuario for u in usuarios):
            return None  # ya existe
        row = {'usuario': usuario, 'contrasena': contrasena, 'rol': rol}
        append_dict_en_csv(self.path, USERS_HEADER, row)
        return row

    def listar_usuarios(self):
        """Devuelve la lista de usuarios (sin mostrar contraseñas si se desea)."""
        return self.cargar()

    def cambiar_contrasena(self, usuario, nueva):
        usuarios = self.cargar()
        cambiado = False
        for u in usuarios:
            if u.get('usuario') == usuario:
                u['contrasena'] = nueva
                cambiado = True
                break
        if cambiado:
            self.escribir_todos(usuarios)
        return cambiado

    def eliminar(self, usuario):
        usuarios = self.cargar()
        nuevos = [u for u in usuarios if u.get('usuario') != usuario]
        if len(nuevos) == len(usuarios):
            return False
        self.escribir_todos(nuevos)
        return True

    def autenticar(self):
        usuarios = self.cargar()
        if not usuarios:
            print('No hay usuarios. Crea al menos un administrador en usuarios.csv')
            return None
        intentos = 0
        while intentos < MAX_LOGIN_INTENTOS:
            user = input('Usuario: ').strip()
            pwd = getpass('Contraseña: ').strip()
            for u in usuarios:
                if u['usuario'] == user and u['contrasena'] == pwd and u['rol'].upper() == 'ADMIN':
                    print('Login correcto.')
                    return u
            intentos += 1
            print('Credenciales incorrectas. Intentos restantes:', MAX_LOGIN_INTENTOS - intentos)
        print('Se excedieron los intentos.')
        return None


class EquipmentManager:
    """CRUD simple para equipos, usando CSV con dicts."""
    def __init__(self, path=EQUIPOS_CSV):
        self.path = path
        asegurar_csv(self.path, EQUIPOS_HEADER)

    def cargar(self):
        return leer_csv_como_dicts(self.path)

    def listar(self):
        return self.cargar()

    def generar_nuevo_id(self):
        equipos = self.cargar()
        ids = []
        for e in equipos:
            try:
                ids.append(int(e.get('equipo_id', 0)))
            except ValueError:
                continue
        return str(max(ids) + 1) if ids else '1'

    def crear(self, nombre, categoria):
        nuevo_id = self.generar_nuevo_id()
        fila = {'equipo_id': nuevo_id, 'nombre_equipo': nombre, 'categoria': categoria, 'estado_actual': 'DISPONIBLE', 'fecha_registro': hoy_str()}
        append_dict_en_csv(self.path, EQUIPOS_HEADER, fila)
        return fila

    def buscar_por_id(self, equipo_id):
        for e in self.cargar():
            if e.get('equipo_id') == str(equipo_id):
                return e
        return None

    def buscar_por_nombre(self, nombre):
        # búsqueda no sensible a mayúsculas
        nombre = nombre.lower()
        return [e for e in self.cargar() if nombre in e.get('nombre_equipo','').lower()]

    def actualizar_estado(self, equipo_id, nuevo_estado):
        equipos = self.cargar()
        cambiado = False
        for e in equipos:
            if e.get('equipo_id') == str(equipo_id):
                e['estado_actual'] = nuevo_estado
                cambiado = True
                break
        if cambiado:
            escribir_dicts_en_csv(self.path, EQUIPOS_HEADER, equipos)
        return cambiado

    def eliminar(self, equipo_id):
        equipos = self.cargar()
        nuevos = [e for e in equipos if e.get('equipo_id') != str(equipo_id)]
        if len(nuevos) == len(equipos):
            return False
        escribir_dicts_en_csv(self.path, EQUIPOS_HEADER, nuevos)
        return True


class LoanManager:
    """Administra solicitudes, aprobaciones, rechazos y devoluciones."""
    def __init__(self, path=PRESTAMOS_CSV):
        self.path = path
        asegurar_csv(self.path, PRESTAMOS_HEADER)

    def cargar(self):
        return leer_csv_como_dicts(self.path)

    def generar_nuevo_id(self):
        prestamos = self.cargar()
        ids = []
        for p in prestamos:
            try:
                ids.append(int(p.get('prestamo_id', 0)))
            except ValueError:
                continue
        return str(max(ids) + 1) if ids else '1'

    def crear_solicitud(self, equipo_id, nombre_equipo, usuario_prestatario, tipo_usuario):
        pid = self.generar_nuevo_id()
        fila = {
            'prestamo_id': pid,
            'equipo_id': str(equipo_id),
            'nombre_equipo': nombre_equipo,
            'usuario_prestatario': usuario_prestatario,
            'tipo_usuario': tipo_usuario.upper(),
            'fecha_solicitud': hoy_str(),
            'fecha_inicio': '',
            'fecha_fin': '',
            'dias': '',
            'retraso': '',
            'estado': 'PENDIENTE',
            'mes': datetime.now().strftime('%m'),
            'anio': datetime.now().strftime('%Y')
        }
        append_dict_en_csv(self.path, PRESTAMOS_HEADER, fila)
        return fila

    def listar_pendientes(self):
        return [p for p in self.cargar() if p.get('estado','').upper() == 'PENDIENTE']

    def aprobar(self, prestamo_id):
        prestamos = self.cargar()
        cambiado = False
        for p in prestamos:
            if p.get('prestamo_id') == str(prestamo_id) and p.get('estado','').upper() == 'PENDIENTE':
                inicio = hoy_str()
                dias = TIEMPO_MAX.get(p.get('tipo_usuario','').upper(), 3)
                fin = sumar_dias(inicio, dias)
                p['fecha_inicio'] = inicio
                p['fecha_fin'] = fin
                p['dias'] = str(dias)
                p['estado'] = 'APROBADO'
                p['mes'] = datetime.now().strftime('%m')
                p['anio'] = datetime.now().strftime('%Y')
                cambiado = True
                break
        if cambiado:
            escribir_dicts_en_csv(self.path, PRESTAMOS_HEADER, prestamos)
        return cambiado

    def rechazar(self, prestamo_id):
        prestamos = self.cargar()
        for p in prestamos:
            if p.get('prestamo_id') == str(prestamo_id) and p.get('estado','').upper() == 'PENDIENTE':
                p['estado'] = 'RECHAZADO'
                escribir_dicts_en_csv(self.path, PRESTAMOS_HEADER, prestamos)
                return True
        return False

    def registrar_devolucion(self, prestamo_id):
        prestamos = self.cargar()
        cambiado = False
        for p in prestamos:
            if p.get('prestamo_id') == str(prestamo_id) and p.get('estado','').upper() == 'APROBADO':
                if not p.get('fecha_inicio'):
                    return False
                dias_usados = dias_entre(p['fecha_inicio'])
                max_dias = TIEMPO_MAX.get(p.get('tipo_usuario','').upper(), 3)
                retraso = max(0, dias_usados - max_dias)
                p['dias'] = str(dias_usados)
                p['retraso'] = str(retraso)
                p['estado'] = 'DEVUELTO'
                p['fecha_fin'] = hoy_str()
                p['mes'] = datetime.now().strftime('%m')
                p['anio'] = datetime.now().strftime('%Y')
                cambiado = True
                break
        if cambiado:
            escribir_dicts_en_csv(self.path, PRESTAMOS_HEADER, prestamos)
        return cambiado

    def prestamos_por_usuario(self, usuario):
        return [p for p in self.cargar() if p.get('usuario_prestatario') == usuario]

    def prestamos_por_equipo(self, equipo_id):
        return [p for p in self.cargar() if p.get('equipo_id') == str(equipo_id)]

# -----------------------------
# Funciones demo y utilidades extra para listas y estructuras
# -----------------------------

def ejemplo_listas_nidimensionales():
    """Ejemplos de listas dentro de listas y cómo recorrerlas."""
    matriz = [[1,2,3],[4,5,6],[7,8,9]]
    print('Matriz:')
    for fila in matriz:
        for valor in fila:
            print(valor, end=' ')
        print()
    # Anidamiento mixto: lista de diccionarios que contienen listas
    data = [
        {'id':1, 'tags':['red','small']},
        {'id':2, 'tags':['blue','large']}
    ]
    print('\nEjemplo de lista de diccionarios con listas internas:')
    for item in data:
        print('id=', item['id'], 'tags:', end=' ')
        for t in item['tags']:
            print(t, end=' ')
        print()

# Funciones útiles para filtrar y comparar

def filtrar_por_categoria(categoria):
    em = EquipmentManager()
    return [e for e in em.listar() if e.get('categoria','').lower() == categoria.lower()]


def contar_por_estado():
    em = EquipmentManager()
    equipos = em.listar()
    resumen = {}
    for e in equipos:
        estado = e.get('estado_actual','').upper()
        resumen[estado] = resumen.get(estado, 0) + 1
    return resumen

# -----------------------------
# Menú principal simplificado y directo
# -----------------------------

def menu_principal():
    um = UserManager()
    em = EquipmentManager()
    lm = LoanManager()

    print('--- TechLab (versión de estudio) ---')
    user = um.autenticar()
    if not user:
        print('Acceso denegado. Finalizando programa.')
        return

    while True:
        print('\n--- MENU ---')
        print('1) Gestionar equipos (crear/listar/buscar/editar/eliminar)')
        print('2) Solicitar préstamo (crea solicitud PENDIENTE)')
        print('3) Revisar pendientes (aprobar/rechazar)')
        print('4) Registrar devolución')
        print('5) Reportes y consultas')
        print('6) Ejemplos de listas y estructuras')
        print('7) Salir')
        opc = input('Elige una opción: ').strip()

        if opc == '1':
            while True:
                print('\n--- Equipos ---')
                print('a) Crear equipo')
                print('b) Listar equipos')
                print('c) Buscar por ID')
                print('d) Buscar por nombre')
                print('e) Editar estado')
                print('f) Eliminar equipo')
                print('v) Volver')
                o = input('Opción equipos: ').strip().lower()
                if o == 'a':
                    nombre = pedir_str_no_vacio('Nombre equipo: ')
                    categoria = pedir_str_no_vacio('Categoría: ')
                    creado = em.crear(nombre, categoria)
                    print('Creado:', creado)
                elif o == 'b':
                    for e in em.listar():
                        print(e)
                elif o == 'c':
                    eid = input('ID: ').strip()
                    r = em.buscar_por_id(eid)
                    print(r or 'No encontrado')
                elif o == 'd':
                    nombre = input('Nombre (o parte): ').strip()
                    res = em.buscar_por_nombre(nombre)
                    for r in res:
                        print(r)
                elif o == 'e':
                    eid = input('ID: ').strip()
                    nuevo = input('Nuevo estado (DISPONIBLE/RESERVADO/PRESTADO): ').strip().upper()
                    ok = em.actualizar_estado(eid, nuevo)
                    print('Estado actualizado' if ok else 'No se actualizó')
                elif o == 'f':
                    eid = input('ID a eliminar: ').strip()
                    ok = em.eliminar(eid)
                    print('Eliminado' if ok else 'No encontrado')
                elif o == 'v':
                    break
                else:
                    print('Opción inválida')

        elif opc == '2':
            eid = input('ID equipo a solicitar: ').strip()
            equipo = em.buscar_por_id(eid)
            if not equipo:
                print('Equipo no existe')
                continue
            if equipo.get('estado_actual','').upper() != 'DISPONIBLE':
                print('Equipo no disponible')
                continue
            usuario_p = pedir_str_no_vacio('Nombre solicitante: ')
            tipo = pedir_str_no_vacio('Tipo usuario (Estudiante/Instructor/Administrativo): ')
            sol = lm.crear_solicitud(eid, equipo.get('nombre_equipo'), usuario_p, tipo)
            em.actualizar_estado(eid, 'RESERVADO')
            print('Solicitud creada:', sol)

        elif opc == '3':
            pendientes = lm.listar_pendientes()
            if not pendientes:
                print('No hay pendientes')
                continue
            for p in pendientes:
                print(p)
            accion = input('Aprobar (A)<id> / Rechazar (R)<id> / V para volver: ').strip()
            if accion.upper().startswith('A'):
                pid = accion[1:].strip()
                if lm.aprobar(pid):
                    # marcar equipo como PRESTADO
                    allp = lm.cargar()
                    target = next((x for x in allp if x['prestamo_id'] == pid), None)
                    if target:
                        em.actualizar_estado(target['equipo_id'], 'PRESTADO')
                    print('Aprobado', pid)
                else:
                    print('No se pudo aprobar')
            elif accion.upper().startswith('R'):
                pid = accion[1:].strip()
                if lm.rechazar(pid):
                    allp = lm.cargar()
                    target = next((x for x in allp if x['prestamo_id'] == pid), None)
                    if target:
                        em.actualizar_estado(target['equipo_id'], 'DISPONIBLE')
                    print('Rechazado', pid)
                else:
                    print('No se pudo rechazar')
            else:
                continue

        elif opc == '4':
            pid = input('Prestamo ID a devolver: ').strip()
            ok = lm.registrar_devolucion(pid)
            if ok:
                allp = lm.cargar()
                target = next((x for x in allp if x['prestamo_id'] == pid), None)
                if target:
                    em.actualizar_estado(target['equipo_id'], 'DISPONIBLE')
                print('Devolución registrada')
            else:
                print('No se pudo registrar devolución')

        elif opc == '5':
            print('Reportes:')
            print('a) Mostrar prestamos por usuario')
            print('b) Mostrar prestamos por equipo')
            print('c) Exportar CSV mensual (manual)')
            r = input('Elige: ').strip().lower()
            if r == 'a':
                user_q = pedir_str_no_vacio('Nombre de usuario: ')
                for p in lm.prestamos_por_usuario(user_q):
                    print(p)
            elif r == 'b':
                eid = input('Equipo ID: ').strip()
                for p in lm.prestamos_por_equipo(eid):
                    print(p)
            elif r == 'c':
                mes = pedir_entero('Mes (1-12): ')
                anio = pedir_entero('Año (YYYY): ')
                prestamos = lm.cargar()
                filtrados = [p for p in prestamos if p.get('mes') == f"{mes:02d}" and p.get('anio') == str(anio)]
                salida = f"reporte_{anio}_{mes}.csv"
                if filtrados:
                    escribir_dicts_en_csv(salida, PRESTAMOS_HEADER, filtrados)
                    print('Exportado', salida)
                else:
                    print('No hay registros para ese periodo')
            else:
                print('Opción inválida')

        elif opc == '6':
            ejemplo_listas_nidimensionales()
            print('\nContar por estado:', contar_por_estado())

        elif opc == '7':
            print('Saliendo...')
            break

        else:
            print('Opción inválida')


if __name__ == '__main__':
    # Antes de iniciar, aseguramos que existan los archivos y una cuenta admin mínima
    asegurar_csv(USERS_CSV, USERS_HEADER)
    asegurar_csv(EQUIPOS_CSV, EQUIPOS_HEADER)
    asegurar_csv(PRESTAMOS_CSV, PRESTAMOS_HEADER)
    # Si no hay usuarios, creamos el admin por defecto
    if not leer_csv_como_dicts(USERS_CSV):
        print('No se encontró usuario administrador. Se creará usuario por defecto: admin/admin')
        append_dict_en_csv(USERS_CSV, USERS_HEADER, {'usuario':'admin','contrasena':'admin','rol':'ADMIN'})

    menu_principal()
