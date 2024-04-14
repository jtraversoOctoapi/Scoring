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
        font-family: Arial, sans-serif; /* O la fuente que prefieras */
    }
    .container {
        width: 100%;
        max-width: 330px;
        padding: 15px;
        margin: auto;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        background: #fff;
        padding: 20px;
        border-radius: 8px;
        box-sizing: border-box; /* Asegura que padding y border estén incluidos en el ancho */
    }
    h1 {
        color: #333;
        text-align: center;
        margin-bottom: 30px;
    }
    form {
        display: flex;
        flex-direction: column;
        gap: 10px; /* Espacio entre los elementos del formulario */
    }
    input, textarea, button {
        width: 100%; /* Ancho completo dentro del contenedor */
        padding: 10px; /* Espaciado interno uniforme */
        margin-bottom: 15px;
        border: 1px solid #ccc;
        border-radius: 4px;
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
