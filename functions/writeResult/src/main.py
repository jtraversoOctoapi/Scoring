from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
import json

# Configuración inicial del cliente de Appwrite
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')  # Tu endpoint de API
client.set_project('661bf232a2d367eccb49')  # Tu ID de proyecto
# Opcional: Configura la sesión si es necesario

database = Databases(client)

def main(req, res, log):
    # Verificar que el método de la solicitud sea POST
    if req.method != 'POST':
        return res.json({'message': 'Invalid request method, POST required'}, 405)

    try:
        body = json.loads(req.body)  # Asegúrate de que se maneje la carga del JSON correctamente
        result = body.get('result')
        path_parts = req.path.split('/')
        
        if len(path_parts) == 3 and path_parts[1] == 'document_id':
            document_id = path_parts[2]
            if document_id and result is not None:
                try:
                    # Actualiza el documento en la base de datos
                    document = database.update_document(
                        database_id='661c0ff748205b5d00b5',
                        collection_id='661c1000c15d1c28d50a',
                        document_id=document_id,
                        data={'respuesta': result},
                        permissions=['read("any")', 'write("any")']
                    )
                    return res.json(document, 200)
                except AppwriteException as e:
                    log(f"Failed to update document: {str(e)}")
                    return res.json({'error': str(e.message)}, 500)
            else:
                return res.json({'message': 'Document ID and result are required'}, 400)
        else:
            return res.json({'message': 'Invalid path'}, 400)
    except Exception as e:
        log(f"Unhandled exception: {str(e)}")
        return res.json({'error': str(e)}, 500)
