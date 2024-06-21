from appwrite.client import Client
from appwrite.services.functions import Functions
import requests

# Configuración inicial del cliente de Appwrite
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')  # Asegúrate de cambiar esto por tu endpoint real
client.set_project('661bf232a2d367eccb49')         # Asegúrate de cambiar esto por tu ID de proyecto real
client.set_key('68a4559f483223bde0c57f0630be9b37191a1a809353da2538a1dcbc3da07039cdf6e9e09a62ae01baa5f026b241981f7cf95ea4be884a12cd95b23d22baae2cc25540fe12cb9655224b0d5c8b7d7022098e7afa558724718032854c413b0d25d08cd6c8615c61e611c6ad83b225f61e4a5bea40ef1b8b4573343bfea693d58a')  # Asegúrate de cambiar esto por tu API key real

def main(context):
    if context.req.method == 'GET':
        # HTML para el formulario
        html_content = """
        <html>
        <head>
            <title>Ingrese RUT</title>
        </head>
        <body>
            <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
                <form action="" method="post">
                    <label for="rut">RUT SIN DV:</label>
                    <input type="text" id="rut" name="rut" required>
                    <button type="submit">Enviar</button>
                </form>
            </div>
        </body>
        </html>
        """
        # Enviar respuesta HTML correctamente sin usar keyword arguments para status o headers
        return context.res.send(html_content, 200, {'content-type': 'text/html'})

    elif context.req.method == 'POST':
        rut = context.req.payload['rut']

        # URL del webhook de Make
        webhook_url = 'https://hook.us1.make.com/pfox96c7uh6tch6csu1vhtv8yl7h4qyb'
        
        # Enviar el RUT al webhook de Make
        response = requests.post(webhook_url, json={"rut": rut})
        
        if response.ok:
            return context.res.json({'message': 'RUT enviado correctamente'})
        else:
            return context.res.json({'error': 'Error al enviar el RUT'}, status_code=response.status_code)
