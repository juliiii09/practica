# restaurant_orders.py
import csv, os, json
from datetime import datetime

ING_CSV = "ingredients.csv"
MENU_CSV = "menu.csv"
ORDERS_CSV = "orders.csv"

ING_HEADER = ["ing_id","name","stock"]
MENU_HEADER = ["dish_id","name","price","ingredients_json"]
ORD_HEADER = ["order_id","dish_id","dish_name","quantity","total_price","date"]

def asegurar(path, header):
    if not os.path.exists(path):
        with open(path,"w",newline="",encoding="utf-8") as f:
            csv.writer(f).writerow(header)

def read_dicts(path):
    if not os.path.exists(path): return []
    with open(path,newline="",encoding="utf-8") as f: return list(csv.DictReader(f))

def write_dicts(path,header,rows):
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=header); w.writeheader(); [w.writerow(r) for r in rows]

def append_dict(path,header,row):
    exists = os.path.exists(path) and os.path.getsize(path)>0
    with open(path,"a",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=header)
        if not exists: w.writeheader()
        w.writerow(row)

# helpers
def next_id(list_dicts,key):
    ids=[] 
    for x in list_dicts:
        try: ids.append(int(x.get(key,0)))
        except: pass
    return str(max(ids)+1) if ids else "1"

# ingredient management
def add_ingredient():
    ings = read_dicts(ING_CSV)
    iid = next_id(ings,"ing_id")
    name = input("Ingrediente nombre: ").strip()
    stock = int(input("Stock (int): ").strip())
    append_dict(ING_CSV,ING_HEADER,{"ing_id":iid,"name":name,"stock":stock}); print("Ingrediente añadido")

# menu/dish management (ingredients stored as JSON string in CSV)
def add_dish():
    menu = read_dicts(MENU_CSV)
    did = next_id(menu,"dish_id")
    name = input("Plato nombre: ").strip()
    price = float(input("Precio: ").strip())
    # pedir ingredientes repetidos: formato list de dicts [{"id":"1","qty":2},...]
    ings = []
    while True:
        ing_id = input("Ingrediente ID (enter para terminar): ").strip()
        if not ing_id: break
        qty = int(input("Cantidad del ingrediente requerida: ").strip())
        ings.append({"id":ing_id,"qty":qty})
    append_dict(MENU_CSV,MENU_HEADER,{"dish_id":did,"name":name,"price":price,"ingredients_json":json.dumps(ings)})
    print("Plato añadido")

def place_order():
    menu = read_dicts(MENU_CSV)
    orders = read_dicts(ORDERS_CSV)
    dish_id = input("Plato ID a ordenar: ").strip()
    dish = next((d for d in menu if d["dish_id"]==dish_id), None)
    if not dish: print("Plato no existe"); return
    qty = int(input("Cantidad: ").strip())
    total = float(dish["price"])*qty
    oid = next_id(orders,"order_id")
    append_dict(ORDERS_CSV,ORD_HEADER,{"order_id":oid,"dish_id":dish_id,"dish_name":dish["name"],"quantity":qty,"total_price":total,"date":datetime.now().strftime("%Y-%m-%d %H:%M")})
    print("Orden generada. Total:", total)

def list_orders(): 
    for o in read_dicts(ORDERS_CSV): print(o)

def menu():
    asegurar(ING_CSV,ING_HEADER); asegurar(MENU_CSV,MENU_HEADER); asegurar(ORDERS_CSV,ORD_HEADER)
    while True:
        print("\\n1) Añadir ingrediente 2) Añadir plato 3) Hacer orden 4) Listar órdenes 0) Salir")
        o=input("Opción: ").strip()
        if o=="1": add_ingredient()
        elif o=="2": add_dish()
        elif o=="3": place_order()
        elif o=="4": list_orders()
        elif o=="0": break
        else: print("Inválido")

if __name__=="__main__": menu()
