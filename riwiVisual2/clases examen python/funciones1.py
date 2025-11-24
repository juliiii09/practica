
"""
def calcularNotaFinal(n1,n2,n3):
    return (n1*0.3)+(n2*0.3)+(n3*0.4)
n1 =float(input("ingresa n1: "))
n2 =float(input("ingresa n2: "))
n3 =float(input("ingresa n3: "))

notaFinal =calcularNotaFinal(n1,n2,n3)
print("la nota final es: ", notaFinal)

"""
"""
#calcular el iva de un producto:
def CalcularIva(precio):
    return (precio * 1.19)
precio= float(input("ingrese el precio del producto: "))


PrecioConIva = CalcularIva(precio)
print(f"el precio final del artuculo es de: {PrecioConIva} ")

"""
"""
def tabla(num):
    print(f"Tabla del {num}:")
    for i in range(1, 13):
        print(f"{num} x {i} = {num * i}")

numero = int(input("Ingrese un número para ver su tabla del 1 al 12: "))
tabla(numero)
"""

"""
lista = []


def calcularPromedio(cantidadDeNotas, notas):
    if cantidadDeNotas == 0:
        return 0
    return sum(notas) / cantidadDeNotas

cantidadDeNotas = int(input("Ingresa la cantidad de notas a agregar: "))
notas = []

for i in range(cantidadDeNotas):
    nota = float(input(f"Ingresa la nota número {i+1}: "))
    notas.append(nota)

promedio = calcularPromedio(cantidadDeNotas, notas)
print(f"El promedio es: {promedio:.2f}")

    """
"""
notas = []

cantidadNotas = int(input("ingresa la cantidad de notas:  "))
for i in range(cantidadNotas):
 nota= float(input(f"ingresa la nota numero {i+1}: "))
 notas.append(nota)

def PromedioNotas(notas, cantidadNotas):
    promedio = sum(notas)/cantidadNotas
    return promedio
    
    
def mayorMenor(notas, cantidadNotas):
    mayor = max(notas)
    menor = min(notas)
    
    return mayor, menor
prom = PromedioNotas(notas, cantidadNotas)
mayor,menor= mayorMenor(notas,cantidadNotas)

print(f"el promedio es: {prom}")
print(f"la nota mayor es:{mayor}")
print(f"la nota menor es: {menor}")
print(f"la lista de notas es {notas}")

"""

"""
precios = []
productos = []

# Pedir cantidad de productos con manejo de errores
while True:
    try:
        cantidadProductos = int(input("¿Cuántos productos vas a ingresar?: "))
        if cantidadProductos <= 0:
            print("La cantidad debe ser un número positivo.")
            continue
        break
    except ValueError:
        print("Error: ingresa un número entero válido.")


# Pedir productos y precios
for i in range(cantidadProductos):

    # Nombre del producto
    producto = input(f"Ingresa el nombre del producto {i+1}: ")
    productos.append(producto)

    # Precio con manejo de errores
    while True:
        try:
            precio = float(input(f"Ingresa el precio de {producto}: "))
            if precio < 0:
                print("El precio no puede ser negativo.")
                continue
            precios.append(precio)
            break
        except ValueError:
            print("Error: debes ingresar un número válido.")


# Función para total
def totalCompra(precios):
    return sum(precios)

# Función para mayor y menor
def precioAltoBajo(precios):
    mayor = max(precios)
    menor = min(precios)
    return mayor, menor


# Mostrar resultados
print("\n--- RESULTADOS ---")
print("Productos:", productos)
print("Precios:", precios)

print("Total de la compra:", totalCompra(precios))

mayor, menor = precioAltoBajo(precios)
print("Precio más alto:", mayor)
print("Precio más bajo:", menor)

   """
   
"""
estudiantes = []
notas = []

while True:
 try:
  cantidadEstudiantes = int(input("ingrese el numero de estudiantes: ")) 
  if cantidadEstudiantes <= 0:
      print("por favor ingrese un numero positivo")
  else:
      #estudiantes.append(cantidadEstudiantes)
      break
 except ValueError:
     print("por favor ingrese un valor valido")
  
    
for i in range(cantidadEstudiantes):
     nombreEstudiante= input(f"por favor ingrese el nombre del estudiante {i+1}: ")
     estudiantes.append(nombreEstudiante)
     
     while True:
      try:
       cantitadNotas = int(input(f"ingrese la cantidad de notas del estudiante {nombreEstudiante}: "))
       if cantitadNotas <=0:
        print("por favor ingresa un valor positivo\n")
       else:
           break
      except ValueError:
          print("por favor ingrese un numero valido")
          
listaNotas = []
for b in range(cantitadNotas):
    while True:
        try:
            nota =float(input(f"ingresa la nota {b+1} del estudiante {nombreEstudiante}:  "))
            if nota <=0 or nota > 5:
                print("por favor ingresa una nota dentro de los valores 1-5")
            else:
                listaNotas.append(nota)
                break
        except ValueError:
            print("ingresaa un valor valido")

notas.append(listaNotas)

def promedioPorEstudiante(listaNotas):
    return sum(listaNotas) / len(listaNotas)

"""


"""
¿Qué es .strip()?

strip() es un método de las cadenas (str) en Python que sirve para quitar espacios en blanco al inicio y al final de un texto.

Ejemplo:

nombre = "   ana   "
---print(nombre.strip())
---nombre = input("Nombre: ").strip()
"""


# gestión simple de estudiantes y sus notas (requiere Python 3.10+ por match/case)

estudiantes = []        # lista de nombres
notas = {}              # diccionario: nombre -> lista de notas


def agregar_estudiantes():
    """Agrega N estudiantes y sus notas."""
    while True:
        try:
            cantidad = int(input("¿Cuántos estudiantes desea agregar?: "))
            if cantidad <= 0:
                print("Por favor ingresa un número mayor que 0.")
                continue
            break
        except ValueError:
            print("Por favor ingrese un valor entero válido.")

    for i in range(cantidad):
        nombre = input(f"Ingrese el nombre del estudiante {len(estudiantes) + 1}: ").strip()
        while not nombre:
            print("El nombre no puede estar vacío.")
            nombre = input(f"Ingrese el nombre del estudiante {len(estudiantes) + 1}: ").strip()

        # evitar duplicados (opcional)
        if nombre in estudiantes:
            print(f"{nombre} ya está registrado. Se actualizarán sus notas.")
        else:
            estudiantes.append(nombre)

        # pedir cantidad de notas para este estudiante
        while True:
            try:
                cantidad_notas = int(input(f"Ingrese la cantidad de notas de {nombre}: "))
                if cantidad_notas <= 0:
                    print("Ingrese un número positivo.")
                    continue
                break
            except ValueError:
                print("Ingrese un número entero válido.")

        # crear lista de notas para este estudiante
        lista_notas = []
        for n in range(cantidad_notas):
            while True:
                try:
                    nota = float(input(f"Ingrese la nota {n+1} de {nombre} (0-5): "))
                    if nota < 0 or nota > 5:
                        print("Ingrese una nota dentro del rango 0-5.")
                        continue
                    lista_notas.append(nota)
                    break
                except ValueError:
                    print("Ingrese un número válido para la nota.")

        # guardar en el diccionario (sobrescribe si ya existía)
        notas[nombre] = lista_notas

    print("Estudiantes y notas guardados correctamente.\n")


def promedio_estudiante(nombre):
    """Devuelve el promedio de un estudiante por nombre (o None si no existe o no tiene notas)."""
    if nombre not in notas:
        return None
    lista = notas[nombre]
    if not lista:
        return None
    return sum(lista) / len(lista)


def promedio_total():
    """Promedio de todas las notas de todos los estudiantes (o None si no hay notas)."""
    todas = []
    for lista in notas.values():
        todas.extend(lista)
    if not todas:
        return None
    return sum(todas) / len(todas)


def mostrar_estudiantes():
    if not estudiantes:
        print("No hay estudiantes registrados.\n")
        return
    print("\n-- Estudiantes registrados --")
    for idx, e in enumerate(estudiantes, start=1):
        print(f"{idx}. {e}")
    print()


def mostrar_notas_por_estudiante():
    if not estudiantes:
        print("No hay estudiantes registrados.\n")
        return
    mostrar_estudiantes()
    nombre = input("Ingrese el nombre del estudiante para ver sus notas: ").strip()
    if nombre in notas:
        print(f"Notas de {nombre}: {notas[nombre]}\n")
    else:
        print("El estudiante no existe o no tiene notas registradas.\n")


def mostrar_promedio_estudiante():
    if not estudiantes:
        print("No hay estudiantes registrados.\n")
        return
    mostrar_estudiantes()
    nombre = input("Ingrese el nombre del estudiante para ver su promedio: ").strip()
    prom = promedio_estudiante(nombre)
    if prom is None:
        print("El estudiante no existe o no tiene notas.\n")
    else:
        print(f"Promedio de {nombre}: {prom:.2f}\n")


def mostrar_promedio_total():
    prom = promedio_total()
    if prom is None:
        print("No hay notas registradas para calcular el promedio total.\n")
    else:
        print(f"Promedio total del curso: {prom:.2f}\n")


def mostrar_menu():
    menu = """
--- MENÚ PRINCIPAL ---
1. Agregar estudiantes y notas
2. Ver lista de estudiantes
3. Ver notas por estudiante
4. Ver promedio de un estudiante
5. Ver promedio total
6. Salir
Elige una opción: """
    return input(menu).strip()


def ejecutar_menu():
    while True:
        opcion = mostrar_menu()
        match opcion:
            case "1":
                agregar_estudiantes()
            case "2":
                mostrar_estudiantes()
            case "3":
                mostrar_notas_por_estudiante()
            case "4":
                mostrar_promedio_estudiante()
            case "5":
                mostrar_promedio_total()
            case "6":
                print("Saliendo... ¡hasta luego!")
                break
            case _:
                print("Opción inválida. Intenta de nuevo.\n")


if __name__ == "__main__":
    ejecutar_menu()

        
        
        
       
  
      
        



    

             