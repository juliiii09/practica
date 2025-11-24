
import csv
import sys


class Inventario:
    #self para acceder a atributos de instancia y otros metodos
    def __init__(self): #init para definir los parametros
        self.productos = []

#agregar productos al inventario

    def agregarProducto(self):
        nombre = input("ingresa el nombre: ")
        try:
            precio = float(input("Precio: "))
            cantidad = int(input("Cantidad: "))
        except:
            print("Valores inválidos.")
            return
        
        #self para guardar los valores en el archivo csv
        self.productos.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})
        print("Producto agregado.\n")

    def mostrarInventario(self):
        if not self.productos:
            print("Inventario vacío.\n")
            return
        for p in self.productos:
            print(p)
        print()

    def buscarProducto(self):
        nombre = input("Nombre a buscar: ")
        for p in self.productos:
            if p["nombre"] == nombre:
                print("Encontrado:", p, "\n")
                return p
        print("No encontrado.\n")
        return  #None

    def actualizarProducto(self):
        p = self.buscarProducto()
        if not p:
            return
        try:
            nuevo_precio = float(input("Nuevo precio: "))
            nueva_cantidad = int(input("Nueva cantidad: "))
        except:
            print("Datos inválidos.\n")
            return
        
        p["precio"] = nuevo_precio
        p["cantidad"] = nueva_cantidad
        print("Producto actualizado.\n")

    def eliminarProducto(self):
        nombre = input("Nombre a eliminar: ")
        for p in self.productos:
            if p["nombre"] == nombre:
                self.productos.remove(p)
                print("Producto eliminado.\n")
                return
        print("No encontrado.\n")

    def calcularEstadisticas(self):
        if not self.productos:
            print("Inventario vacío.\n")
            return
        
        unidadesTotales = sum(p["cantidad"] for p in self.productos)
        valorTotal = sum(p["precio"] * p["cantidad"] for p in self.productos)
        masCaro = max(self.productos, key=lambda p: p["precio"])
        mayorStock = max(self.productos, key=lambda p: p["cantidad"])

        print("Estadísticas")
        print("Unidades totales:", unidadesTotales)
        print("Valor total:", valorTotal)
        print("Más caro:", masCaro["nombre"], masCaro["precio"])
        print("Mayor stock:", mayorStock["nombre"], mayorStock["cantidad"])
        print()

    def guardarCsv(self):
        if not self.productos:
            print("Inventario vacío.\n")
            return
        
        ruta = input("Ruta para guardar (ej: inventario.csv): ")
        try:
            with open(ruta, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["nombre", "precio", "cantidad"])
                for p in self.productos:
                    writer.writerow([p["nombre"], p["precio"], p["cantidad"]])
            print("Inventario guardado.\n")
        except:
            print("Error al guardar.\n")


# cargar el csv con una ruta

    def cargarCsv(self):
        ruta = input("Ruta del archivo: ")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)  
                cargados = []
                for fila in reader:
                    if len(fila) != 3:
                        continue
                    try:
                        cargados.append({
                            "nombre": fila[0],
                            "precio": float(fila[1]),
                            "cantidad": int(fila[2])
                        })
                    except:
                        continue
            self.productos = cargados
            print("Inventario cargado.\n")
        except FileNotFoundError:
            print("Archivo no encontrado.\n")
        except:
            print("Error al cargar.\n")



def menu():
    inv = Inventario()

    while True:
        print("MENU PRINCIPAL")
        print("1. Agregar producto")
        print("2. Mostrar inventario")
        print("3. Buscar producto")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Estadísticas")
        print("7. Guardar CSV")
        print("8. Cargar CSV")
        print("9. Salir")

        op = input("Opción: ")

        if op == "1": inv.agregarProducto()
        elif op == "2": inv.mostrarInventario()
        elif op == "3": inv.buscarProducto()
        elif op == "4": inv.actualizarProducto()
        elif op == "5": inv.eliminarProducto()
        elif op == "6": inv.calcularEstadisticas()
        elif op == "7": inv.guardarCsv()
        elif op == "8": inv.cargarCsv()
        elif op == "9":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.\n")

menu()
