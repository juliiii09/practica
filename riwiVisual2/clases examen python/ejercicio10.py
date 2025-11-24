# ecommerce_orders.py
# E-commerce CLI simple: productos, pedidos, devoluciones, reportes

import csv, os, json
from datetime import datetime
from shutil import copyfile

PRODUCTS_CSV = "products.csv"
ORDERS_CSV = "orders.csv"
PRODUCTS_HEADER = ["product_id","name","price","stock"]
ORDERS_HEADER = ["order_id","items_json","total","date","estado"]

def asegurar(path, header):
    if not os.path.exists(path):
        with open(path,"w",newline="",encoding="utf-8") as f: csv.writer(f).writerow(header)

def read(path):
    if not os.path.exists(path): return []
    with open(path,newline="",encoding="utf-8") as f: return list(csv.DictReader(f))

def write(path, header, rows):
    if os.path.exists(path): copyfile(path, path+".bak")
    with open(path,"w",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header); w.writeheader(); [w.writerow(r) for r in rows]

def append(path, header, row):
    ex = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path,"a",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header)
        if not ex: w.writeheader()
        w.writerow(row)

def next_id(rows, key):
    ids=[]
    for r in rows:
        try: ids.append(int(r[key])); 
        except: pass
    return str(max(ids)+1) if ids else "1"

# Productos
def add_product():
    products = read(PRODUCTS_CSV)
    pid = next_id(products,"product_id")
    name = input("Nombre producto: ").strip()
    price = float(input("Precio: ").strip() or "0")
    stock = int(input("Stock: ").strip() or "0")
    append(PRODUCTS_CSV, PRODUCTS_HEADER, {"product_id":pid,"name":name,"price":str(price),"stock":str(stock)})
    print("Producto agregado")

def list_products():
    for p in read(PRODUCTS_CSV): print(p)

def update_stock(pid, qty):
    products = read(PRODUCTS_CSV)
    for p in products:
        if p["product_id"]==pid:
            p["stock"] = str(int(p["stock"]) + int(qty))
            write(PRODUCTS_CSV, PRODUCTS_HEADER, products)
            return True
    return False

# Pedidos
def create_order():
    products = read(PRODUCTS_CSV)
    cart = []
    total = 0.0
    while True:
        pid = input("Product ID (enter para finalizar): ").strip()
        if not pid: break
        prod = next((p for p in products if p["product_id"]==pid), None)
        if not prod:
            print("Producto no existe"); continue
        qty = int(input("Cantidad: ").strip() or "1")
        if int(prod["stock"]) < qty:
            print("Stock insuficiente"); continue
        cart.append({"product_id":pid,"name":prod["name"],"qty":qty,"price":float(prod["price"])})
        total += qty * float(prod["price"])
    if not cart:
        print("Carrito vacío"); return
    orders = read(ORDERS_CSV)
    oid = next_id(orders,"order_id")
    append(ORDERS_CSV, ORDERS_HEADER, {"order_id":oid,"items_json":json.dumps(cart),"total":str(total),"date":datetime.now().strftime("%Y-%m-%d"), "estado":"COMPLETADO"})
    # restar stock
    for item in cart:
        for p in products:
            if p["product_id"] == item["product_id"]:
                p["stock"] = str(int(p["stock"]) - int(item["qty"]))
    write(PRODUCTS_CSV, PRODUCTS_HEADER, products)
    print("Pedido creado:", oid, "Total:", total)

def list_orders():
    for o in read(ORDERS_CSV):
        print(o)

def process_return(order_id):
    orders = read(ORDERS_CSV); products = read(PRODUCTS_CSV)
    for o in orders:
        if o["order_id"] == order_id and o["estado"] == "COMPLETADO":
            items = json.loads(o["items_json"])
            # reponer stock
            for it in items:
                for p in products:
                    if p["product_id"] == it["product_id"]:
                        p["stock"] = str(int(p["stock"]) + int(it["qty"]))
            o["estado"] = "DEVUELTO"
            write(PRODUCTS_CSV, PRODUCTS_HEADER, products)
            write(ORDERS_CSV, ORDERS_HEADER, orders)
            print("Devolución procesada para pedido", order_id)
            return
    print("Pedido no encontrado o ya devuelto")

# Reportes
def sales_by_day():
    orders = read(ORDERS_CSV)
    agg = {}
    for o in orders:
        day = o["date"]
        agg[day] = agg.get(day, 0.0) + float(o.get("total",0))
    for day, val in sorted(agg.items()):
        print(day, val)

def menu():
    asegurar(PRODUCTS_CSV, PRODUCTS_HEADER); asegurar(ORDERS_CSV, ORDERS_HEADER)
    while True:
        print("\\n--- ECOMMERCE ---")
        print("1) Agregar producto 2) Listar productos 3) Crear pedido 4) Listar pedidos 5) Devolver pedido 6) Ventas por día 0) Salir")
        op = input("Opción: ").strip()
        if op=="1": add_product()
        elif op=="2": list_products()
        elif op=="3": create_order()
        elif op=="4": list_orders()
        elif op=="5": process_return(input("Order ID: ").strip())
        elif op=="6": sales_by_day()
        elif op=="0": break
        else: print("Inválido")

if __name__=="__main__":
    menu()
