from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
import json

# Configuración inicial del cliente de Appwrite
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1') \
    .set_project('661bf232a2d367eccb49') \
    .set_key('68a4559f483223bde0c57f0630be9b37191a1a809353da2538a1dcbc3da07039cdf6e9e09a62ae01baa5f026b241981f7cf95ea4be884a12cd95b23d22baae2cc25540fe12cb9655224b0d5c8b7d7022098e7afa558724718032854c413b0d25d08cd6c8615c61e611c6ad83b225f61e4a5bea40ef1b8b4573343bfea693d58a')

database = Databases(client)

def main(context):
    # Verificar que el método de la solicitud sea POST
    if context.req.method != 'POST':
        return context.res.json({'message': 'Invalid request method, POST required'}, 405)

    try:
        body = context.req.body
        result = body.get('result')
        path_parts = context.req.path.split('/')
        
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
                    return context.res.json(document, 200)
                except AppwriteException as e:
                    context.log(f"Failed to update document: {str(e)}")
                    return context.res.json({'error': str(e.message)}, 500)
            else:
                return context.res.json({'message': 'Document ID and result are required'}, 400)
        else:
            return context.res.json({'message': 'Invalid path'}, 400)
    except Exception as e:
        context.log(f"Unhandled exception: {str(e)}")
        return context.res.json({'error': str(e)}, 500)
