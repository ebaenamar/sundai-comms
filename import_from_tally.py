import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv('.env.temp')  # Cargamos el archivo con la API key de Tally

# Configuración
TALLY_API_KEY = os.getenv('TALLY_API_KEY')
TALLY_FORM_ID = os.getenv('TALLY_FORM_ID')
BACKEND_URL = os.getenv('BACKEND_URL', 'https://tally-subscriber-api.onrender.com')

def get_all_tally_submissions():
    """Obtiene todos los envíos de un formulario de Tally"""
    print(f"Obteniendo envíos del formulario {TALLY_FORM_ID} de Tally...")
    
    url = f"https://api.tally.so/forms/{TALLY_FORM_ID}/submissions"
    headers = {
        "Authorization": f"Bearer {TALLY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    all_submissions = []
    
    try:
        # Obtener la primera página
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data:
            all_submissions.extend(data['data'])
            print(f"Página 1: {len(data['data'])} envíos")
            
            # Manejar paginación si es necesario
            # (La API de Tally podría tener paginación, ajusta según sea necesario)
            
        return all_submissions
        
    except Exception as e:
        print(f"Error al obtener envíos de Tally: {e}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Respuesta del servidor: {e.response.text}")
        return []

def import_to_postgres(submissions):
    """Importa los envíos a la base de datos PostgreSQL"""
    imported = 0
    errors = 0
    
    print(f"\nImportando {len(submissions)} envíos a PostgreSQL...")
    
    for i, submission in enumerate(submissions, 1):
        try:
            # Extraer email y nombre del envío de Tally
            email = None
            name = None
            
            # Buscar campos de email y nombre en los datos del formulario
            for field in submission.get('fields', []):
                field_key = field.get('key', '').lower()
                field_type = field.get('type', '').upper()
                field_value = field.get('value')
                
                if field_type == 'EMAIL' or 'email' in field_key:
                    email = field_value
                elif 'name' in field_key or 'nombre' in field_key:
                    name = field_value
            
            if not email:
                print(f"\n[{i}/{len(submissions)}] Advertencia: No se encontró email en el envío {submission.get('id')}")
                errors += 1
                continue
            
            # Crear el payload para la API
            payload = {
                "data": {
                    "formId": submission.get('formId', ''),
                    "formName": submission.get('formName', ''),
                    "fields": submission.get('fields', [])
                }
            }
            
            # Mostrar progreso
            print(f"\n[{i}/{len(submissions)}] Procesando: {email} - {name or 'Sin nombre'}")
            
            # Enviar al webhook
            response = requests.post(
                f"{BACKEND_URL}/api/webhook/tally",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print(f"   ✓ Importado correctamente")
                imported += 1
            else:
                print(f"   ✗ Error al importar: {response.status_code} - {response.text}")
                errors += 1
                
        except Exception as e:
            print(f"\n[{i}/{len(submissions)}] Error al procesar envío: {e}")
            errors += 1
    
    return imported, errors

def main():
    print("=== Importador de envíos de Tally a PostgreSQL ===\n")
    
    # Verificar configuración
    if not TALLY_API_KEY or not TALLY_FORM_ID:
        print("Error: Faltan variables de configuración. Por favor verifica el archivo .env.temp")
        return
    
    print(f"Configuración:")
    print(f"- Formulario Tally ID: {TALLY_FORM_ID}")
    print(f"- Backend URL: {BACKEND_URL}")
    
    # Obtener envíos de Tally
    submissions = get_all_tally_submissions()
    
    if not submissions:
        print("No se encontraron envíos para importar")
        return
    
    print(f"\nSe encontraron {len(submissions)} envíos en Tally")
    
    # Mostrar vista previa
    print("\nVista previa de los primeros 3 envíos:")
    for i, sub in enumerate(submissions[:3], 1):
        email = next((f.get('value') for f in sub.get('fields', []) 
                     if f.get('type') == 'EMAIL' or 'email' in f.get('key', '').lower()), 'No email')
        name = next((f.get('value') for f in sub.get('fields', []) 
                    if 'name' in f.get('key', '').lower() or 'nombre' in f.get('key', '').lower()), 'Sin nombre')
        print(f"{i}. {email} - {name}")
    
    # Preguntar confirmación
    confirm = input("\n¿Deseas continuar con la importación? (s/n): ")
    if confirm.lower() != 's':
        print("Importación cancelada")
        return
    
    # Importar a PostgreSQL
    imported, errors = import_to_postgres(submissions)
    
    # Mostrar resumen
    print("\n=== Resumen de la importación ===")
    print(f"Total de envíos en Tally: {len(submissions)}")
    print(f"Importados correctamente: {imported}")
    print(f"Errores: {errors}")
    
    # Verificar la base de datos después de la importación
    if imported > 0:
        print("\nVerificando la base de datos...")
        try:
            response = requests.get(f"{BACKEND_URL}/api/subscribers/")
            if response.status_code == 200:
                subscribers = response.json()
                print(f"\nTotal de suscriptores en la base de datos: {len(subscribers)}")
                if subscribers:
                    print("\nÚltimos suscriptores:")
                    for sub in subscribers[:5]:  # Mostrar solo los primeros 5
                        print(f"- {sub.get('email')}: {sub.get('name', 'Sin nombre')}")
        except Exception as e:
            print(f"Error al verificar la base de datos: {e}")

if __name__ == "__main__":
    main()
