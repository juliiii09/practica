# data_pipeline_clean_analyze.py
# Pipeline: carga, limpieza, derivación y resumen de CSV

import csv, os, json
from statistics import mean, median

# --- Ajusta estas variables a tu dataset ---
INPUT_CSV = "raw_data.csv"   # coloca aquí tu CSV de entrada
OUTPUT_CSV = "cleaned.csv"
SUMMARY_JSON = "summary.json"

# columnas esperadas (ejemplo)
REQUIRED_FIELDS = ["id","name","qty","price","category"]
NUMERIC_FIELDS = ["qty","price"]

# -------------------------
# Funciones reutilizables
# -------------------------
def load_csv(path):
    """Carga CSV y devuelve lista de dicts."""
    if not os.path.exists(path):
        print("Archivo no existe:", path); return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def clean_data(rows):
    """Limpieza básica:
       - quitar filas con campos obligatorios vacíos
       - convertir numéricos
       - rellenar valores por defecto
    """
    out = []
    for r in rows:
        skip = False
        for req in REQUIRED_FIELDS:
            if req not in r or r[req] is None or str(r[req]).strip() == "":
                skip = True; break
        if skip: continue
        # convertir numéricos
        for nf in NUMERIC_FIELDS:
            try: r[nf] = float(r.get(nf,0))
            except: r[nf] = 0.0
        # normalizar texto
        r["category"] = r.get("category","").strip().lower()
        out.append(r)
    return out

def derive_columns(rows):
    """Agregar columna total = qty * price y category_short."""
    for r in rows:
        r["total"] = r.get("qty",0) * r.get("price",0)
        r["category_short"] = (r.get("category","")[:10]).lower()
    return rows

def summarize(rows):
    """Generar resumen: medias, medianas, conteo por categoría."""
    vals = [r.get("total",0) for r in rows]
    summary = {}
    summary["count"] = len(rows)
    summary["mean_total"] = mean(vals) if vals else 0
    summary["median_total"] = median(vals) if vals else 0
    # conteo por categoria
    cat_counts = {}
    for r in rows:
        cat_counts[r["category"]] = cat_counts.get(r["category"], 0) + 1
    summary["by_category"] = cat_counts
    return summary

def export_csv(path, rows):
    """Exportar a CSV, infiriendo cabeceras de la primera fila."""
    if not rows:
        print("No hay filas para exportar"); return
    keys = list(rows[0].keys())
    with open(path,"w",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
        for r in rows: w.writerow(r)
    print("Exportado a", path)

def export_json(path, obj):
    with open(path,"w",encoding="utf-8") as f: json.dump(obj, f, ensure_ascii=False, indent=2)
    print("Resumen exportado a", path)

# -------------------------
# Flujo principal
# -------------------------
def pipeline():
    rows = load_csv(INPUT_CSV)
    print("Filas cargadas:", len(rows))
    cleaned = clean_data(rows)
    print("Filas después de limpieza:", len(cleaned))
    derived = derive_columns(cleaned)
    summary = summarize(derived)
    export_csv(OUTPUT_CSV, derived)
    export_json(SUMMARY_JSON, summary)
    print("Pipeline completado. Resumen:", summary)

if __name__ == "__main__":
    pipeline()

"""
Crea un script que:

Importe un CSV arbitrario (se asume que tiene columnas numéricas y textuales).

Limpie datos: eliminar filas con campos obligatorios vacíos, convertir tipos, rellenar nulos con valores por defecto.

Añada columnas derivadas (por ejemplo: total = qty * price, categoria_normalizada = lower+strip).

Genere reportes: medias, medianas, conteos por categoría, exporte a cleaned.csv y a summary.json.

Tener funciones modulares load_csv, clean_data, derive_columns, summarize, export_csv, export_json.

Muy útiles para examen en la sección de manipulación de datos.


"""