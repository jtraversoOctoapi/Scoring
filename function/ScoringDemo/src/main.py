import os
import requests
from appwrite.query import Query
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from urllib.parse import parse_qs
from .templates import html_template

# Initialize the Appwrite client
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1') \
    .set_project('661bf232a2d367eccb49') \
    .set_key('68a4559f483223bde0c57f0630be9b37191a1a809353da2538a1dcbc3da07039cdf6e9e09a62ae01baa5f026b241981f7cf95ea4be884a12cd95b23d22baae2cc25540fe12cb9655224b0d5c8b7d7022098e7afa558724718032854c413b0d25d08cd6c8615c61e611c6ad83b225f61e4a5bea40ef1b8b4573343bfea693d58a')

# Initialize the database client
database = Databases(client)

def main(context):
    if context.req.method == 'GET':
        return context.res.send(html_template, 200, {'content-type': 'text/html'})
    
    # Utiliza .get() para acceder al encabezado 'content-type' y normaliza el nombre del encabezado a minúsculas
    content_type = context.req.headers.get('content-type', '').lower()
    
    if context.req.method == 'POST' and 'application/x-www-form-urlencoded' in content_type:
        formData = parse_qs(context.req.body)
        rut = formData.get('rut', [''])[0]
        email = formData.get('email', [''])[0]
        
        # Crea un nuevo documento en la colección
        document = database.create_document(
            database_id='661c0ff748205b5d00b5',
            collection_id='661c1000c15d1c28d50a',
            document_id=ID.unique(), 
            data={'rut': rut, 'email': email},
        )
        
        # Extrae el ID del nuevo documento
        document_id = document['$id']
        created_at = document['$createdAt']
        
        # Datos para enviar al webhook, incluyendo el ID del documento
        data_to_send = {
            'rut': rut,
            'email': email,
            'document_id': document_id,
            'created_at': created_at
        }
        
        # URL del webhook
        webhook_url = 'https://hook.us1.make.com/iq7pr5ib62ct8pin9qxwsxf5jh2v3w3m'
        try:
            # Enviar los datos al webhook y capturar la respuesta
            response = requests.post(webhook_url, json=data_to_send)
            if response.status_code == 200:
                    return context.res.json({"message": "Datos enviados correctamente al webhook", "response": response.text}, status=200)
            else:
                return context.res.json({"error": "Error en el proceso del webhook.", "status_code": response.status_code}, status=response.status_code)
        except Exception as e:
            response_message = f"Ocurrió un error al procesar la solicitud: {str(e)}"
            return context.res.send(response_message, 400, {'Content-Type': 'text/plain'})
    else:
        error_message = {
            "error": True,
            "message": "Método o tipo de contenido no permitido.",
            "method_received": context.req.method,
            "content_type_received": content_type
        }
        return context.res.json(error_message, 400)
