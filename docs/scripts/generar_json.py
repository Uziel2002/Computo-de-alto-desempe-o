from elasticsearch import Elasticsearch
import json
import os

# Configura tu API Key y endpoint de Elastic Cloud
ELASTIC_CLOUD_ID = "172f9438c56f434f9c52a102fa1c2fe3:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQzNDkxNjUwMGQxYWQ0YjVlODgxYjI1ODFkOTgyZGYwOCQxMjcxOTMyMGM5ZDg0OTkwOTEzNzc2YzlhMjRkZThmZQ=="  # lo obtienes del panel de Elastic Cloud
API_KEY = "MEdZYXo1WUJ1MFVPdHhXRUowUUY6ZTU5RDhTVWtreEFwSUY5aTYwVTdyUQ"            # generado desde Kibana

# Conexión al cliente de Elasticsearch
es = Elasticsearch(
    cloud_id=ELASTIC_CLOUD_ID,
    api_key=API_KEY
)

# Consulta al índice (ajusta el nombre si es distinto)
INDEX_NAME = "muertes_mexico"
QUERY = {
    "size": 1000,
    "sort": [{"date": "asc"}],
    "_source": ["date", "deaths"]
}

# Ejecuta la consulta
response = es.search(index=INDEX_NAME, body=QUERY)

# Extrae los datos
datos = [
    {
        "date": hit["_source"]["date"],
        "deaths": hit["_source"]["deaths"]
    }
    for hit in response["hits"]["hits"]
]

# Guarda el JSON en la carpeta que usa GitHub Pages
output_dir = "docs/data"
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, "muertes_mx_clean.json"), "w", encoding="utf-8") as f:
    json.dump(datos, f, indent=2, ensure_ascii=False)

print(f"Archivo JSON generado con {len(datos)} registros en {output_dir}/muertes_mx_clean.json")
