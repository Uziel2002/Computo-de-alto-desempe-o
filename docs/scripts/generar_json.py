import pandas as pd
import os
import json
import re

print("Directorio actual:", os.getcwd())

# Crear el directorio de datos si no existe
os.makedirs("data", exist_ok=True)

# Ruta al archivo CSV - ajusta esto según la ubicación real de tu CSV
csv_path = "C:/Users/uziel/OneDrive/Documentos/Computo-de-alto-desempe-o/docs/data/muertes_mx.csv"

try:
    # Leer el archivo CSV 
    df = pd.read_csv(csv_path, encoding="latin1")

    # Imprimir las primeras filas para verificar el formato original
    print("Primeras filas antes de la conversión:")
    print(df.head())

    # Verificar y convertir la columna 'date'
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%y', errors='coerce')
        df = df[df['date'].notna()]  # Filtrar fechas inválidas
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    else:
        print("Advertencia: No se encontró la columna 'date'. Se omitirá la conversión de fechas.")

    # Limpiar nombres de columnas (minúsculas, sin espacios ni caracteres especiales)
    df.columns = [
        re.sub(r'\W+', '_', col.strip().lower())
        for col in df.columns
    ]

    # Convertir columna 'deaths' a entero si existe
    if 'deaths' in df.columns:
        df['deaths'] = pd.to_numeric(df['deaths'], errors='coerce').fillna(0).astype(int)

    # Asegurarse de que la columna 'date' esté ordenada si existe
    if 'date' in df.columns:
        df = df.sort_values(by="date")

    # Ruta de salida del JSON
    output_json = "/docs/data/muertes_mx_clean.json"

    # Guardar como lista de objetos JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(df.to_dict(orient="records"), f, ensure_ascii=False, indent=2)

    print(f"✅ Archivo JSON generado correctamente en: {output_json}")
    print(f"🔢 {len(df)} registros procesados.")
    print("🧾 Columnas exportadas:", df.columns.tolist())

except FileNotFoundError:
    print(f"⚠️ Error: No se encontró el archivo CSV en {csv_path}")
    print("Generando datos de muestra...")

    # Datos de muestra
    sample_data = [
        {"date": "2020-01-01", "deaths": 1200},
        {"date": "2020-02-01", "deaths": 1150},
        {"date": "2020-03-01", "deaths": 1300},
        {"date": "2020-04-01", "deaths": 1500},
        {"date": "2020-05-01", "deaths": 1800},
        {"date": "2020-06-01", "deaths": 2100},
        {"date": "2020-07-01", "deaths": 2300},
        {"date": "2020-08-01", "deaths": 2100},
        {"date": "2020-09-01", "deaths": 1900},
        {"date": "2020-10-01", "deaths": 1700},
        {"date": "2020-11-01", "deaths": 1600},
        {"date": "2020-12-01", "deaths": 1500}
    ]

    # Guardar datos de muestra
    with open("data/muertes_mx_clean.json", 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)

    print("✅ Archivo JSON con datos de muestra generado en: data/muertes_mx_clean.json")

except Exception as e:
    print(f"❌ Error al procesar el archivo: {e}")
