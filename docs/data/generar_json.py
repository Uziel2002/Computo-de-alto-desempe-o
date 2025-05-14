import pandas as pd
import os

print("Directorio actual:", os.getcwd())

# Leer el archivo CSV
df = pd.read_csv("C:/Users/uziel/OneDrive/Documentos/Computo-de-alto-desempe-o/docs/data/muertes_mx.csv", encoding="latin1")

# Imprimir las primeras filas para verificar el formato de las fechas
print(df.head())

# Convertir la columna 'date' a datetime con el formato 'DD-MM-YY'
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%y', errors='coerce')  # Convertir 'date' a datetime

# Verificar si la conversión fue correcta
print(df.head())

# Convertir las fechas a formato de cadena (en lugar de timestamp)
df['date'] = df['date'].dt.strftime('%Y-%m-%d')  # Convertir la fecha a 'YYYY-MM-DD'

# Limpiar los nombres de las columnas (en minúsculas, sin espacios y caracteres especiales)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('+', 'plus').str.replace('/', '_')

# Asegurarse de que la columna 'date' sea tipo datetime y ordenarlo por esta columna
df = df.sort_values(by="date")

# Crear el directorio si no existe
output_dir = "docs/data"
os.makedirs(output_dir, exist_ok=True)

# Guardar el archivo JSON
df.to_json(f"{output_dir}/muertes_mx_clean.json", orient="records", lines=True)

print("Archivo JSON generado correctamente.")
