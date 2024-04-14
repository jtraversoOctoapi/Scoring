import os
import requests
from appwrite.query import Query
from urllib.parse import parse_qs

html = '''
<!doctype html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulario de Scoring</title>
    <link rel="stylesheet" href="https://unpkg.com/pico.css">
</head>
<body>
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
</body>
</html>
'''

def main(context):
    if context.req.method == 'GET':
        return context.res.send(html, 200, {'content-type': 'text/html'})

    # Utiliza .get() para acceder al encabezado 'content-type' y normaliza el nombre del encabezado a minúsculas
    content_type = context.req.headers.get('content-type', '').lower()
    
    if context.req.method == 'POST' and 'application/x-www-form-urlencoded' in content_type:
        formData = parse_qs(context.req.body.decode('utf-8'))

        message = {
            'rut': formData.get('rut', [''])[0],
            'email': formData.get('email', [''])[0],
        }
        # URL del webhook
        webhook_url = 'https://hook.us1.make.com/5i1vm5745y7guaewm9np9uyaneitygk8'
        try:
          # Enviar los datos al webhook y capturar la respuesta
          response = requests.post(webhook_url, json=message)
          if response.status_code == 200:
            response_message = "Datos enviados correctamente al webhook."
          else:
            response_message = "Error en el proceso del webhook."
        except Exception as e:
          response_message = f"Ocurrió un error al procesar la solicitud: {str(e)}"
        
        return context.res.send(response_message, 200, {'Content-Type': 'text/plain'})
        #return context.res.send(str(message))  # Asegúrate de convertir el diccionario a string para enviarlo

    return context.res.send('Not found', 404, {'Content-Type': 'text/plain'})
