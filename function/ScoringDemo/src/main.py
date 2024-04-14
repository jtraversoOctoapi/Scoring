import os
import requests
from appwrite.query import Query
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
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
<script>
    document.addEventListener('DOMContentLoaded', function () {
        function openModal(response) {
            document.getElementById('responseText').value = response;
            document.getElementById('modal').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('modal').style.display = 'none';
        }

        function formDataToUrlEncoded(formElement) {
            const formData = new FormData(formElement);
            const pairs = [];
            for (const [key, value] of formData) {
                pairs.push(`${encodeURIComponent(key)}=${encodeURIComponent(value)}`);
            }
            return pairs.join('&');
        }

        document.querySelector('form').addEventListener('submit', function (e) {
            e.preventDefault();
            var formData = new FormData(this);
            console.log('URL de acción:', this.action);
            const urlEncodedData = formDataToUrlEncoded(this);
            for (var pair of formData.entries()) {
                console.log(pair[0]+ ': ' + pair[1]);  // Muestra cada campo del formulario y su valor
            }
            document.getElementById('loader').style.display = 'block'; // Mostrar el loader
            console.log('Esperando el resultado de su evaluación...'); // Añadir console.log para depuración
            
            fetch(this.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: urlEncodedData
            })
            .then(response => {
                console.log('Respuesta recibida', response);
                console.log('Estado de la respuesta:', response.status);
                if (response.ok) {
                    return response.json();
                } else {
                    response.text().then(text => console.error('Error en la respuesta:', text)); // Muestra el cuerpo de la respuesta como texto si no es un JSON válido
                    throw new Error('Respuesta del servidor no contiene el formato correcto');
                }
            })
            .then(data => {
                console.log('Datos recibidos', data); // Añadir console.log para ver los datos recibidos
                if (data && data.document_id) {
                    checkForResponse(data.document_id); // Comienza a verificar la respuesta
                } else {
                    console.error('document_id no está presente en la respuesta');
                }
            })
            .catch(error => {
                console.error('Error al enviar formulario:', error);
            });
        });
    });

    function checkForResponse(documentId) {
        console.log('Verificando respuesta para el documento', documentId); // Añadir console.log para depuración
        const interval = setInterval(() => {
            fetch(`https://661c32a7cbb49de418a6.appwrite.global/documents/${documentId}`)
            .then(response => response.json())
            .then(data => {
                console.log('Verificación de datos', data); // Añadir console.log para ver los datos de la verificación
                if (data.respuesta !== null) {
                    clearInterval(interval); // Detiene las comprobaciones
                    document.getElementById('loader').style.display = 'none'; // Ocultar el loader
                    openModal(data.respuesta); // Abre el modal con la respuesta
                }
            })
            .catch(error => {
                console.error('Error al consultar el documento:', error);
            });
        }, 2000); // Consulta cada 2 segundos
    }
</script>
    <style>
        body,
        html {
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
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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

        input,
        button {
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

        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: none;
            align-items: center;
            justify-content: center;
        }

        .modal-content {
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            width: 80%;
            max-width: 600px;
        }

        textarea {
            width: 100%;
            height: 300px;
            /* Ajuste según necesites */
            overflow-y: scroll;
        }

        #loader {
            position: fixed;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            font-size: 20px;
            color: white;
            background-color: rgba(0, 0, 0, 0.8);
            padding: 20px;
            border-radius: 10px;
            z-index: 1000;
            /* Añade un borde y animación */
            border: 6px solid #f3f3f3;
            border-top: 6px solid #3498db;
            width: 50px;
            height: 50px;
            animation: spin 2s linear infinite;
        }

        /* Animación de giro */
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="modal" id="modal">
        <div class="modal-content">
            <h1>Respuesta de la Evaluación</h1>
            <textarea readonly id="responseText"></textarea>
            <button onclick="closeModal()">Cerrar</button>
        </div>
    </div>
    <div id="loader" style="display: none;">
        Cargando...
    </div>
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
                try:
                    # Intentamos parsear la respuesta JSON
                    response_json = response.json()
                    return context.res.json({"message": "Datos enviados correctamente al webhook.", "data": response_json}, status=200)
                except ValueError:
                    # Si no es JSON, enviamos un mensaje estándar
                    return context.res.json({"message": "Datos enviados correctamente al webhook, pero la respuesta no era JSON.", "response": response.text}, status=200)
            else:
                return context.res.json({"error": "Error en el proceso del webhook.", "status_code": response.status_code}, status=response.status_code)
        except Exception as e:
            response_message = f"Ocurrió un error al procesar la solicitud: {str(e)}"
            return context.res.send(response_message, 200, {'Content-Type': 'text/plain'})
    else:
        error_message = {
            "error": True,
            "message": "Método o tipo de contenido no permitido.",
            "method_received": context.req.method,
            "content_type_received": content_type
        }
        return context.res.json(error_message, 400)
