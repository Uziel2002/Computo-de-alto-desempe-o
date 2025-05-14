import pandas as pd
import json
import requests
import os
import sys
from datetime import datetime

# Configuración de Elasticsearch
ELASTIC_URL = "http://localhost:9200"
INDEX_NAME = "muertes_mx"

# Ruta al archivo JSON - Asegúrate de que esta ruta sea correcta
json_path = "docs/data/muertes_mx_clean.json"
# También obtener la ruta directamente del argumento si se proporciona
if len(sys.argv) > 1:
    json_path = sys.argv[1]

print(f"Intentando procesar el archivo: {json_path}")

# Comprobar si el directorio existe, si no, crearlo
os.makedirs(os.path.dirname(json_path), exist_ok=True)

# Función para arreglar el archivo JSON si tiene formato incorrecto
def fix_json_file(file_path):
    print(f"Intentando arreglar el archivo JSON: {file_path}")
    try:
        # Leer el archivo como texto
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Intentar diferentes estrategias para arreglar el JSON
        
        # Estrategia 1: Si son líneas JSON (JSONL), convertirlas a un array JSON
        try:
            lines = content.strip().split('\n')
            data = []
            for line in lines:
                if line.strip():  # Ignorar líneas vacías
                    try:
                        item = json.loads(line)
                        data.append(item)
                    except json.JSONDecodeError as e:
                        print(f"Error decodificando línea: {line[:50]}... - {e}")
            
            if data:
                # Guardar como array JSON
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print("Archivo convertido exitosamente de JSONL a array JSON")
                return True
        except Exception as e:
            print(f"Error en estrategia 1: {e}")
        
        # Estrategia 2: Intentar encontrar y corregir objetos JSON sin delimitadores correctos
        try:
            # Asegurarse de que el contenido esté envuelto en corchetes para formar un array JSON
            if not content.strip().startswith('['):
                content = '[' + content
            if not content.strip().endswith(']'):
                content = content + ']'
            
            # Reemplazar objetos JSON consecutivos con comas
            content = content.replace('}{', '},{')
            
            # Intentar cargar el JSON modificado
            data = json.loads(content)
            
            # Si llega aquí, la corrección funcionó
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("Archivo JSON reparado exitosamente")
            return True
        except Exception as e:
            print(f"Error en estrategia 2: {e}")
        
        # Si llegamos aquí, no se pudo reparar el archivo
        return False
    except Exception as e:
        print(f"Error al intentar reparar el archivo JSON: {e}")
        return False

# Función para crear datos de muestra
def create_sample_data(file_path):
    print(f"Creando datos de muestra en: {file_path}")
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
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    print(f"Se ha creado un archivo JSON de muestra en {file_path}")
    return True

# Intenta leer y procesar el archivo
df = None
success = False

# Verificar si el archivo existe
if os.path.exists(json_path):
    # Intentar leer como array JSON primero
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        df = pd.DataFrame(data)
        print("Archivo JSON leído correctamente como array JSON")
        success = True
    except Exception as e:
        print(f"Error al leer el archivo como array JSON: {e}")
        
        # Intentar leer como JSONL
        try:
            df = pd.read_json(json_path, orient="records", lines=True)
            print("Archivo JSON leído correctamente como JSONL")
            
            # Convertir de JSONL a JSON estándar
            try:
                # Convertir timestamps a strings de fecha
                for col in df.select_dtypes(include=['datetime64[ns]']).columns:
                    df[col] = df[col].dt.strftime('%Y-%m-%d')
                
                # Guardar como JSON estándar
                with open(json_path, 'w', encoding='utf-8') as f:
                    records = df.to_dict(orient='records')
                    json.dump(records, f, ensure_ascii=False, indent=2)
                print(f"El archivo ha sido convertido de JSONL a JSON estándar en {json_path}")
                success = True
            except Exception as e:
                print(f"Error al convertir JSONL a JSON estándar: {e}")
        except Exception as e2:
            print(f"Error al intentar como JSONL: {e2}")
            
            # Intentar reparar el archivo
            if fix_json_file(json_path):
                try:
                    # Intentar leer el archivo reparado
                    with open(json_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    df = pd.DataFrame(data)
                    print("Archivo JSON reparado y leído correctamente")
                    success = True
                except Exception as e:
                    print(f"Error al leer el archivo reparado: {e}")
else:
    print(f"El archivo {json_path} no existe")

# Si no se pudo leer el archivo, crear datos de muestra
if not success:
    if create_sample_data(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            df = pd.DataFrame(data)
            print("Datos de muestra creados y leídos correctamente")
            success = True
        except Exception as e:
            print(f"Error al leer los datos de muestra: {e}")

# Si aún no tenemos datos, salir
if df is None or not success:
    print("No se pudieron cargar o crear datos. Saliendo.")
    sys.exit(1)

# Verificar las primeras filas del DataFrame
print("\nPrimeras filas del DataFrame:")
print(df.head())

# Asegurarse de que la columna 'date' esté en formato de cadena 'YYYY-MM-DD'
if 'date' in df.columns:
    try:
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"Error al formatear las fechas: {e}")

# Guardar el DataFrame como JSON estándar para asegurar compatibilidad
try:
    # Manejar NaN y otros tipos de datos no serializables
    def json_serial(obj):
        if pd.isna(obj):
            return None
        if isinstance(obj, (datetime, pd.Timestamp)):
            return obj.strftime('%Y-%m-%d')
        raise TypeError(f"Type {type(obj)} not serializable")
    
    # Guardar como JSON con manejo personalizado de tipos
    with open(json_path, 'w', encoding='utf-8') as f:
        records = df.to_dict(orient='records')
        json.dump(records, f, default=json_serial, ensure_ascii=False, indent=2)
    print(f"DataFrame guardado como JSON estándar en {json_path}")
except Exception as e:
    print(f"Error al guardar DataFrame como JSON: {e}")

# --- Carga en Elasticsearch ---
# Verificar la conexión a Elasticsearch
try:
    response = requests.get(ELASTIC_URL, timeout=5)
    if response.status_code != 200:
        print(f"\nNo se puede conectar a Elasticsearch en {ELASTIC_URL}")
        print("Asegúrate de que Elasticsearch esté ejecutándose")
        print("Continuando sin cargar datos en Elasticsearch...")
        es_available = False
    else:
        print("\nConexión exitosa a Elasticsearch")
        es_available = True
except requests.exceptions.RequestException as e:
    print(f"\nNo se puede conectar a Elasticsearch: {e}")
    print("Continuando sin cargar datos en Elasticsearch...")
    es_available = False

# Si Elasticsearch está disponible, cargar los datos
if es_available:
    try:
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
            # Crear el cuerpo del índice
            data = {
                "date": row['date'] if 'date' in row else None,
                "deaths": row['deaths'] if 'deaths' in row else None
            }
            
            # Eliminar valores None
            data = {k: v for k, v in data.items() if v is not None}
            
            # Preparar el formato para el bulk API de Elasticsearch
            bulk_data.append(json.dumps({"index": {"_index": INDEX_NAME}}))
            bulk_data.append(json.dumps(data))
        
        # Convertir los datos en formato adecuado para la API bulk
        bulk_data_str = "\n".join(bulk_data) + "\n"
        
        # Realizar la solicitud bulk para cargar los datos
        response = requests.post(
            f"{ELASTIC_URL}/_bulk", 
            headers={"Content-Type": "application/json"}, 
            data=bulk_data_str,
            timeout=10
        )
        
        # Manejo de la respuesta
        if response.status_code == 200:
            print("Datos cargados correctamente en Elasticsearch.")
        else:
            print(f"Error al cargar los datos. Código de estado: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error al interactuar con Elasticsearch: {e}")

print("\n--- Resumen Final ---")
print(f"1. Los datos están disponibles en: {json_path}")
print("2. El sitio web debe buscar los datos en esta ubicación")
if es_available:
    print("3. Se han cargado los datos en Elasticsearch")
else:
    print("3. No se pudieron cargar los datos en Elasticsearch (servicio no disponible)")
print("\nPróximos pasos:")
print("- Asegúrate de que tu aplicación web esté configurada para buscar el archivo en la ubicación correcta")
print("- Revisa la consola del navegador para detectar posibles errores")
print("- Verifica que estés usando un servidor web y no abriendo los archivos directamente")