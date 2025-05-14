import json
import requests

# URL y nombre del índice de Elasticsearch
ELASTIC_URL = "http://localhost:9200"  # Asegúrate de que esté en el puerto correcto
INDEX_NAME = "muertes_mx"

# Comprobar si el índice existe antes de intentar eliminarlo
response = requests.head(f"{ELASTIC_URL}/{INDEX_NAME}")
if response.status_code == 200:
    delete_response = requests.delete(f"{ELASTIC_URL}/{INDEX_NAME}")
    if delete_response.status_code == 200:
        print(f"Índice '{INDEX_NAME}' eliminado correctamente.")
    else:
        print(f"Error al eliminar el índice: {delete_response.status_code} - {delete_response.text}")
else:
    print(f"El índice '{INDEX_NAME}' no existe, no se necesita eliminar.")

# Cargar el archivo JSON
with open("docs/data/muertes_mx_clean.json", "r") as file:
    lines = file.readlines()

# Construir los datos para el formato bulk
bulk_data = []
for line in lines:
    bulk_data.append(json.dumps({"index": {"_index": INDEX_NAME}}))
    bulk_data.append(line.strip())  # Elimina posibles saltos de línea adicionales

# Asegurarse de que la última línea termine con un salto de línea
bulk_data_str = "\n".join(bulk_data) + "\n"  # Añadir salto de línea al final

# Realizar la solicitud POST para cargar los datos a Elasticsearch
response = requests.post(f"{ELASTIC_URL}/_bulk", headers={"Content-Type": "application/json"}, data=bulk_data_str)

# Manejo de la respuesta
if response.status_code == 200:
    print("Datos cargados correctamente en Elasticsearch.")
    print(response.json())  # Imprimir la respuesta JSON para ver detalles
else:
    print(f"Error al cargar los datos. Código de estado: {response.status_code}")
    print(response.text)  # Imprimir el cuerpo de la respuesta de error