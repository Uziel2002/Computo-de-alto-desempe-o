import pandas as pd
import os

print("Directorio actual:", os.getcwd())

# Leer el archivo CSV
df = pd.read_csv("C:/Users/uziel/OneDrive/Documentos/Computo-de-alto-desempe-o/docs/data/muertes_mx.csv", encoding="latin1")

# Limpiar los nombres de las columnas (en minúsculas, sin espacios y caracteres especiales)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '').str.replace('+', 'plus').str.replace('/', '')

# Asegurarse de que la columna 'date' sea tipo datetime y ordenarlo por esta columna
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Convertir 'date' a datetime
df = df.sort_values(by="date")

# Crear el directorio si no existe
output_dir = "docs/data"
os.makedirs(output_dir, exist_ok=True)

# Guardar el archivo JSON
df.to_json(f"{output_dir}/muertes_mx_clean.json", orient="records", lines=True)

print("Archivo JSON generado correctamente.")