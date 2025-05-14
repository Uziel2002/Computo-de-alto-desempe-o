import pandas as pd
import json
import requests

# Configuración de Elasticsearch
ELASTIC_URL = "http://localhost:9200"  # Asegúrate de que el puerto sea el correcto
INDEX_NAME = "muertes_mx"

# Leer el archivo JSON
df = pd.read_json("docs/data/muertes_mx_clean.json", orient="records", lines=True)

# Verificar las primeras filas del DataFrame
print("Primeras filas del archivo JSON:")
print(df.head())

# Asegurarse de que la columna 'date' esté en formato de cadena 'YYYY-MM-DD' (en caso de que no lo esté)
df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

# Eliminar el índice actual si existe
response = requests.head(f"{ELASTIC_URL}/{INDEX_NAME}")
if response.status_code == 200:
    delete_response = requests.delete(f"{ELASTIC_URL}/{INDEX_NAME}")
    if delete_response.status_code == 200:
        print(f"Índice '{INDEX_NAME}' eliminado correctamente.")
    else:
        print(f"Error al eliminar el índice: {delete_response.status_code} - {delete_response.text}")
else:
    print(f"El índice '{INDEX_NAME}' no existe, no se necesita eliminar.")

# Preparar los datos para el formato bulk de Elasticsearch
bulk_data = []
for _, row in df.iterrows():
    # Crear el cuerpo del índice (reemplaza 'date' y 'deaths' con los nombres de tus columnas)
    data = {
        "date": row['date'],
        "deaths": row['deaths']
    }
    
    # Preparar el formato para el bulk API de Elasticsearch
    bulk_data.append(json.dumps({"index": {"_index": INDEX_NAME}}))
    bulk_data.append(json.dumps(data))

# Convertir los datos en formato adecuado para la API bulk
bulk_data_str = "\n".join(bulk_data) + "\n"

# Realizar la solicitud bulk para cargar los datos
response = requests.post(f"{ELASTIC_URL}/_bulk", headers={"Content-Type": "application/json"}, data=bulk_data_str)

# Manejo de la respuesta
if response.status_code == 200:
    print("Datos cargados correctamente en Elasticsearch.")
    print(response.json())  # Imprimir detalles de la respuesta de Elasticsearch
else:
    print(f"Error al cargar los datos. Código de estado: {response.status_code}")
    print(response.text)  # Imprimir el cuerpo de la respuesta de error
