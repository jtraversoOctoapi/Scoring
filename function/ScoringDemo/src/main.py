from appwrite.query import Query
from urllib.parse import parse_qs
import os

html = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Contact Form</title>
  </head>
  <body>
    <form action="/" method="POST">
      <input type="text" id="name" name="name" placeholder="Name" required>
      <input type="email" id="email" name="email" placeholder="Email" required>
      <textarea id="content" name="content" placeholder="Message" required></textarea>
      <button type="submit">Submit</button>
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
        formData = parse_qs(context.req.body)

        message = {
            'name': formData.get('name', [''])[0],
            'email': formData.get('email', [''])[0],
            'content': formData.get('content', [''])[0]
        }

        return context.res.send(str(message))  # Asegúrate de convertir el diccionario a string para enviarlo

    return context.res.send('Not found', 404)
