
import pandas as pd
from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Conexión con Elastic Cloud
es = Elasticsearch(
    cloud_id=os.environ["ELASTIC_CLOUD_ID"],
    basic_auth=(os.environ["ELASTIC_USERNAME"], os.environ["ELASTIC_PASSWORD"])
)

# Cargar CSV
df = pd.read_csv("amazon_echo_dot.csv")

# Subir a Elasticsearch
for _, row in df.iterrows():
    doc = {
        "rating": row["rating"],
        "review": row.get("reviewText", ""),
        "date": row.get("reviewTime", datetime.now().isoformat())
    }
    es.index(index="echo-reviews", document=doc)

# Consultar los datos
res = es.search(index="echo-reviews", size=1000, query={"match_all": {}})
hits = res["hits"]["hits"]

# Procesar: conteo de reviews por rating
ratings = [hit["_source"]["rating"] for hit in hits]
counts = pd.Series(ratings).value_counts().sort_index()

# Graficar
plt.figure(figsize=(8, 4))
counts.plot(kind='bar')
plt.title("Distribución de Ratings")
plt.xlabel("Rating")
plt.ylabel("Cantidad de Reviews")
plt.tight_layout()

# Guardar imagen
os.makedirs("output", exist_ok=True)
plt.savefig("output/index.png")

# Crear HTML
with open("output/index.html", "w") as f:
    f.write(f"""
    <html>
    <head><title>Gráfico Echo Dot</title></head>
    <body>
        <h1>Distribución de Ratings</h1>
        <img src="index.png" />
    </body>
    </html>
    """)
