from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
import json

# Configuración inicial del cliente de Appwrite
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')
client.set_project('661bf232a2d367eccb49')
client.set_key('your_api_key_here')

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
        document = database.get_document('661c0ff748205b5d00b5', '661c1000c15d1c28d50a', document_id)
        if 'respuesta' in document:
            response_data = json.loads(document['respuesta'])
            basic_info = {key: response_data[key] for key in ['rut', 'email', 'monto', 'plazo', 'Lista Negra', 'Lista Blanca', 'estado_credito', 'total_deudas', 'score_credito']}
            
            # Asegurarse de parsear correctamente el campo Resultado Pricing que es una cadena JSON dentro de otra cadena
            if 'Resultado Pricing' in response_data:
                pricing_results = json.loads(response_data['Resultado Pricing'])
            else:
                pricing_results = []

            # Utilizar una plantilla HTML adecuada para renderizar la salida
            html_content = html_template.render(basic_info=basic_info, pricing_results=pricing_results)
            return context.res.send(html_content, 200, {'content-type': 'text/html'})
        else:
            return context.res.json({'message': 'No response data available'}, 404)

    except AppwriteException as e:
        return context.res.json({'error': str(e.message)}, 500)
    except json.JSONDecodeError as e:
        return context.res.json({'error': 'JSON decoding error: ' + str(e)}, 500)
    except Exception as e:
        return context.res.json({'error': 'Unhandled exception: ' + str(e)}, 500)

