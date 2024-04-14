import os
import requests
from appwrite.query import Query
from appwrite.client import Client
from appwrite.services.databases import Databases
from urllib.parse import parse_qs

# Initialize the Appwrite client
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1') \
    .set_project('661bf232a2d367eccb49') \
    .set_key('68a4559f483223bde0c57f0630be9b37191a1a809353da2538a1dcbc3da07039cdf6e9e09a62ae01baa5f026b241981f7cf95ea4be884a12cd95b23d22baae2cc25540fe12cb9655224b0d5c8b7d7022098e7afa558724718032854c413b0d25d08cd6c8615c61e611c6ad83b225f61e4a5bea40ef1b8b4573343bfea693d58a')

# Initialize the database client
database = Databases(client)

html = '''
<!doctype html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DEMO SCORING</title>
    <link rel="stylesheet" href="https://unpkg.com/pico.css">
    <style>
    body, html {
        height: 100%;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        background-color: #f4f4f8;
        font-family: Arial, sans-serif;
    }
    .container {
        width: 100%;
        max-width: 330px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        background: #fff;
        border-radius: 8px;
        box-sizing: border-box;
    }
    h1 {
        color: #333;
        text-align: center;
        margin-bottom: 30px;
    }
    form {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    input, button {
        width: calc(100% - 20px);
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
    }
    button {
        background-color: #007bff;
        color: white;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    button:hover {
        background-color: #0056b3;
    }
    </style>
</head>
<body>
    <div class="container">
        <h1>DEMO SCORING</h1>
        <form method="POST">
            <div>
                <label for="rut">RUT del Cliente:</label>
                <input type="text" id="rut" name="rut" required>
            </div>
            <div>
                <label for="email">Email del Cliente:</label>
                <input type="email" id="email" name="email" required>
            </div>
            <button type="submit">Enviar</button>
        </form>
    </div>
</body>
</html>

'''

def main(context):
    if context.req.method == 'GET':
        return context.res.send(html, 200, {'content-type': 'text/html'})

    # Utiliza .get() para acceder al encabezado 'content-type' y normaliza el nombre del encabezado a minúsculas
    content_type = context.req.headers.get('content-type', '').lower()
    
    if context.req.method == 'POST' and 'application/x-www-form-urlencoded' in content_type:
        formData = parse_qs(context.req.body)
        rut: formData.get('rut', [''])[0]
        email: formData.get('email', [''])[0]

        # Crea un nuevo documento en la colección
        document = database.create_document(
            '661c1000c15d1c28d50a',  # Reemplaza con el ID de tu colección
            {'rut': rut, 'email': email},
            read=['*'],  # Ajusta según las reglas de acceso que necesites
            write=['*']
        )

        # Extrae el ID del nuevo documento
        document_id = document['$id']

        # Datos para enviar al webhook, incluyendo el ID del documento
        data_to_send = {
            'rut': rut,
            'email': email,
            'document_id': document_id
        }

        # URL del webhook
        webhook_url = 'https://hook.us1.make.com/5i1vm5745y7guaewm9np9uyaneitygk8'
        try:
          # Enviar los datos al webhook y capturar la respuesta
          response = requests.post(webhook_url, json=data_to_send)
          if response.status_code == 200:
            response_message = "Datos enviados correctamente al webhook."
          else:
            response_message = "Error en el proceso del webhook."
        except Exception as e:
          response_message = f"Ocurrió un error al procesar la solicitud: {str(e)}"
        
        return context.res.send(response_message, 200, {'Content-Type': 'text/plain'})
        #return context.res.send(str(message))  # Asegúrate de convertir el diccionario a string para enviarlo

    return context.res.send('Not found', 404, {'Content-Type': 'text/plain'})
