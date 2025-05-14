  // Función para cargar los datos desde Elasticsearch
  async function loadData() {
    const elasticUrl = "https://34916500d1ad4b5e881b2581d982df08.us-central1.gcp.cloud.es.io:443";
    const indexName = "muertes_mx"; 
    const apiKey = "MEdZYXo1WUJ1MFVPdHhXRUowUUY6ZTU5RDhTVWtreEFwSUY5aTYwVTdyUQ=="; 

    try {
      const response = await fetch(`${elasticUrl}/${indexName}/_search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `ApiKey ${apiKey}`
        },
        body: JSON.stringify({
          size: 1000,
          query: { match_all: {} },
          sort: [{ date: "asc" }]
        })
      });

      if (response.ok) {
        const json = await response.json();
        return json.hits.hits.map(hit => hit._source);
      } else {
        console.warn("Fallo en la consulta a Elasticsearch. Usando datos de muestra.");
        return sampleData;
      }
    } catch (error) {
      console.error("Error al conectarse a Elasticsearch:", error);
      return sampleData;
    }
  }
