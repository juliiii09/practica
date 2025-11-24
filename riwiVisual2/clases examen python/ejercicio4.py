# matrices_y_operaciones.py
# Entradas por consola: crear matriz, sumar filas/columnas, transponer y buscar un valor.

def pedir_entero(prompt, minimo=None):
    while True:
        v = input(prompt).strip()
        try:
            n = int(v)
            if minimo is not None and n < minimo:
                print("Debes ingresar un número >= ", minimo)
                continue
            return n
        except:
            print("Escribe un entero válido.")

def crear_matriz():
    filas = pedir_entero("Número de filas: ", 1)
    cols = pedir_entero("Número de columnas: ", 1)
    matriz = []
    print("Ingresa los valores fila por fila:")
    for i in range(filas):
        fila = []
        for j in range(cols):
            valor = pedir_entero(f"valor[{i}][{j}]: ")
            fila.append(valor)
        matriz.append(fila)
    return matriz

def mostrar_matriz(m):
    print("Matriz:")
    for fila in m:
        print(fila)

def sumar_filas(m):
    return [sum(fila) for fila in m]

def sumar_columnas(m):
    if not m: return []
    cols = len(m[0])
    result = []
    for j in range(cols):
        s = 0
        for i in range(len(m)):
            s += m[i][j]
        result.append(s)
    return result

def transponer(m):
    if not m: return []
    cols = len(m[0])
    t = []
    for j in range(cols):
        fila = []
        for i in range(len(m)):
            fila.append(m[i][j])
        t.append(fila)
    return t

def buscar_valor(m, objetivo):
    pos = []
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == objetivo:
                pos.append((i,j))
    return pos

def menu():
    matriz = []
    while True:
        print("\n--- MATRICES ---")
        print("1 Crear matriz")
        print("2 Mostrar")
        print("3 Sumar filas")
        print("4 Sumar columnas")
        print("5 Transponer")
        print("6 Buscar valor")
        print("0 Salir")
        op = input("Opción: ").strip()
        if op == "1":
            matriz = crear_matriz()
        elif op == "2":
            mostrar_matriz(matriz)
        elif op == "3":
            print("Suma por fila:", sumar_filas(matriz))
        elif op == "4":
            print("Suma por columna:", sumar_columnas(matriz))
        elif op == "5":
            print("Transpuesta:")
            mostrar_matriz(transponer(matriz))
        elif op == "6":
            objetivo = pedir_entero("Valor a buscar: ")
            print("Posiciones:", buscar_valor(matriz, objetivo))
        elif op == "0":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
