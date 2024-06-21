from appwrite.client import Client
from appwrite.services.functions import Functions

def main(req, res):
    if req.method == 'GET':
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
        return res.html(html_content)
    
    if req.method == 'POST':
        rut = req.payload['rut']

        # URL del webhook
        webhook_url = 'https://hook.us1.make.com/pfox96c7uh6tch6csu1vhtv8yl7h4qyb'
        
        # Enviar el RUT al webhook de Make
        response = requests.post(webhook_url, json={"rut": rut})
        
        if response.status_code == 200:
            return res.json({'message': 'RUT enviado correctamente'})
        else:
            return res.json({'error': 'Error al enviar el RUT'}, status_code=response.status_code)

# Configuración del cliente de Appwrite (ajustar según sea necesario)
client = Client()
client.set_endpoint('https://[YOUR_API_ENDPOINT]/v1')  # Tu Endpoint de Appwrite
client.set_project('[YOUR_PROJECT_ID]')  # Tu Project ID
client.set_key('[YOUR_API_KEY]')  # Tu API Key

functions = Functions(client)
