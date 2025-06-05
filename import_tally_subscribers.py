import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env.temp
load_dotenv('.env.temp')

# Configuración
TALLY_API_KEY = os.getenv('TALLY_API_KEY')
TALLY_FORM_ID = os.getenv('TALLY_FORM_ID')
BACKEND_URL = os.getenv('BACKEND_URL')

def get_tally_subscribers():
    """Obtiene todos los envíos del formulario de Tally"""
    print(f"Obteniendo suscriptores del formulario {TALLY_FORM_ID}...")
    
    url = f"https://api.tally.so/forms/{TALLY_FORM_ID}/submissions"
    headers = {"Authorization": f"Bearer {TALLY_API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except Exception as e:
        print(f"Error al obtener suscriptores de Tally: {e}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Respuesta del servidor: {e.response.text}")
        return []

def import_to_postgres(subscribers):
    """Importa los suscriptores a la base de datos PostgreSQL"""
    imported = 0
    errors = 0
    
    print(f"\nImportando {len(subscribers)} suscriptores a PostgreSQL...")
    
    for i, sub in enumerate(subscribers, 1):
        try:
            # Extraer email y nombre del envío de Tally
            email = None
            name = None
            
            # Buscar campos de email y nombre en los datos del formulario
            for field in sub.get('fields', []):
                field_key = field.get('key', '').lower()
                field_type = field.get('type', '').upper()
                field_value = field.get('value')
                
                if field_type == 'EMAIL' or 'email' in field_key:
                    email = field_value
                elif 'name' in field_key or 'nombre' in field_key:
                    name = field_value
            
            if not email:
                print(f"\n[{i}/{len(subscribers)}] Advertencia: No se encontró email en el envío {sub.get('id')}")
                errors += 1
                continue
            
            # Crear el payload para la API
            payload = {
                "data": {
                    "formId": sub.get('formId', ''),
                    "formName": sub.get('formName', ''),
                    "fields": sub.get('fields', [])
                }
            }
            
            # Mostrar progreso
            print(f"\n[{i}/{len(subscribers)}] Procesando: {email} - {name or 'Sin nombre'}")
            
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
            print(f"\n[{i}/{len(subscribers)}] Error al procesar suscriptor: {e}")
            errors += 1
    
    return imported, errors

def main():
    print("=== Importador de suscriptores de Tally a PostgreSQL ===\n")
    
    # Verificar configuración
    if not all([TALLY_API_KEY, TALLY_FORM_ID, BACKEND_URL]):
        print("Error: Faltan variables de configuración. Por favor verifica el archivo .env.temp")
        return
    
    print(f"Configuración:")
    print(f"- Formulario Tally ID: {TALLY_FORM_ID}")
    print(f"- Backend URL: {BACKEND_URL}")
    
    # Obtener suscriptores de Tally
    subscribers = get_tally_subscribers()
    
    if not subscribers:
        print("No se encontraron suscriptores para importar")
        return
    
    print(f"\nSe encontraron {len(subscribers)} suscriptores en Tally")
    
    # Preguntar confirmación
    confirm = input("¿Deseas continuar con la importación? (s/n): ")
    if confirm.lower() != 's':
        print("Importación cancelada")
        return
    
    # Importar a PostgreSQL
    imported, errors = import_to_postgres(subscribers)
    
    # Mostrar resumen
    print("\n=== Resumen de la importación ===")
    print(f"Total de suscriptores en Tally: {len(subscribers)}")
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
