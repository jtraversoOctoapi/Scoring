from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
from .templates import html_template  # Asegúrate de tener una plantilla HTML adecuada para renderizar la salida
import json

# Configuración inicial del cliente de Appwrite
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1') \
    .set_project('661bf232a2d367eccb49') \
    .set_key('68a4559f483223bde0c57f0630be9b37191a1a809353da2538a1dcbc3da07039cdf6e9e09a62ae01baa5f026b241981f7cf95ea4be884a12cd95b23d22baae2cc25540fe12cb9655224b0d5c8b7d7022098e7afa558724718032854c413b0d25d08cd6c8615c61e611c6ad83b225f61e4a5bea40ef1b8b4573343bfea693d58a')

database = Databases(client)

def main(context):
    if context.req.method != 'GET':
        return context.res.json({'message': 'Invalid request method, GET required'}, 405)

    path_parts = context.req.path.split('/')
    if len(path_parts) != 3 or path_parts[1] != 'document_id':
        return context.res.json({'message': 'Invalid path format'}, 400)

    document_id = path_parts[2]
    if not document_id:
        return context.res.json({'message': 'Document ID is required'}, 400)

    try:
        # Recupera el documento especificado
        document = database.get_document('661c0ff748205b5d00b5', '661c1000c15d1c28d50a', document_id)
        response_data = json.loads(document['respuesta']) if isinstance(document['respuesta'], str) else document['respuesta']

        # Preparar datos para renderizar en la plantilla HTML
        basic_info = {key: response_data[key] for key in ['rut', 'email', 'monto', 'plazo', 'Lista Negra', 'Lista Blanca', 'estado_credito', 'total_deudas', 'score_credito']}
        pricing_results = json.loads(response_data.get('Resultado Pricing', '[]'))

        # Renderizar la página HTML con los datos
        html_content = html_template.render(basic_info=basic_info, pricing_results=pricing_results)
        return context.res.send(html_content, 200, {'content-type': 'text/html'})

    except AppwriteException as e:
        return context.res.json({'error': str(e.message)}, 500)

    except Exception as e:
        return context.res.json({'error': str(e)}, 500)
