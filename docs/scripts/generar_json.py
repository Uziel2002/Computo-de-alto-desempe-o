import pandas as pd
import os
import json

print("Directorio actual:", os.getcwd())

# Crear el directorio de datos si no existe
os.makedirs("data", exist_ok=True)

# Ruta al archivo CSV - ajusta esto según la ubicación real de tu CSV
csv_path = "data/muertes_mx.csv"

try:
    # Leer el archivo CSV 
    df = pd.read_csv(csv_path, encoding="latin1")

    # Imprimir las primeras filas para verificar el formato de las fechas
    print("Primeras filas antes de la conversión:")
    print(df.head())

    # Convertir la columna 'date' a datetime con el formato 'DD-MM-YY'
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%y', errors='coerce')

    # Verificar si la conversión fue correcta
    print("Primeras filas después de la conversión a datetime:")
    print(df.head())

    # Convertir las fechas a formato de cadena (en lugar de timestamp)
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')  # Convertir la fecha a 'YYYY-MM-DD'

    # Limpiar los nombres de las columnas (en minúsculas, sin espacios y caracteres especiales)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('+', 'plus').str.replace('/', '_')

    # Asegurarse de que la columna 'date' esté ordenada
    df = df.sort_values(by="date")

    # Crear la ruta de salida del JSON
    output_json = "data/muertes_mx_clean.json"

    # Guardar el archivo JSON como array (no como JSONL)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(df.to_dict(orient="records"), f, ensure_ascii=False, indent=2)

    print(f"Archivo JSON generado correctamente en {output_json}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo CSV en {csv_path}")
    print("Generando datos de muestra...")
    
    # Crear datos de muestra si el archivo original no se encuentra
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
    
    # Guardar los datos de muestra como JSON
    output_json = "data/muertes_mx_clean.json"
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    print(f"Archivo JSON con datos de muestra generado en {output_json}")

except Exception as e:
    print(f"Error al procesar el archivo: {e}")