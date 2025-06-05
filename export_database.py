import requests
import json
from datetime import datetime

def export_database():
    """Exporta todos los datos de la base de datos a un archivo JSON"""
    print("Exportando base de datos...")
    
    # Obtener todos los suscriptores
    print("Obteniendo suscriptores...")
    response = requests.get("https://tally-subscriber-api.onrender.com/api/subscribers/")
    
    if response.status_code != 200:
        print(f"Error al obtener suscriptores: {response.status_code} - {response.text}")
        return
    
    subscribers = response.json()
    print(f"Se encontraron {len(subscribers)} suscriptores")
    
    # Obtener todos los envíos de formularios
    print("\nObteniendo envíos de formularios...")
    response = requests.get("https://tally-subscriber-api.onrender.com/api/submissions/")
    
    submissions = []
    if response.status_code == 200:
        submissions = response.json()
        print(f"Se encontraron {len(submissions)} envíos de formularios")
    else:
        print(f"No se pudieron obtener los envíos de formularios: {response.status_code} - {response.text}")
    
    # Crear el diccionario con los datos
    export_data = {
        "exported_at": datetime.utcnow().isoformat(),
        "subscribers": subscribers,
        "submissions": submissions
    }
    
    # Guardar en un archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tally_subscribers_export_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nExportación completada. Datos guardados en: {filename}")
    print(f"Total suscriptores: {len(subscribers)}")
    print(f"Total envíos: {len(submissions)}")
    
    # Mostrar una vista previa
    print("\nVista previa de los datos exportados:")
    print(json.dumps({
        "exported_at": export_data["exported_at"],
        "subscribers_count": len(export_data["subscribers"]),
        "submissions_count": len(export_data["submissions"]),
        "subscribers_sample": export_data["subscribers"][:2] if export_data["subscribers"] else []
    }, indent=2))

if __name__ == "__main__":
    export_database()
