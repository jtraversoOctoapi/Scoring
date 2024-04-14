import AppwriteService from './appwrite.js';
import { generateShortCode, throwIfMissing } from './utils.js';

export default async ({ res, req, log, error }) => {
  throwIfMissing(process.env, [
    'APPWRITE_API_KEY',
    'APPWRITE_DATABASE_ID',
    'APPWRITE_COLLECTION_ID',
  ]);

  const appwrite = new AppwriteService();

module.exports = async function (req, res) {
    const fetch = require('node-fetch');
    const { method, payload } = req;

    if (method === 'GET') {
        // Servir el HTML cuando se accede a la función via GET
        res
            .setHeader('Content-Type', 'text/html')
            .send(`
<!DOCTYPE html>
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
`);
    } else if (method === 'POST') {
        // Procesar el formulario cuando se envía via POST
        const { rut, email } = JSON.parse(payload);

        // Aquí colocas la lógica para llamar al webhook de Make.com
        const response = await fetch('https://hook.us1.make.com/5i1vm5745y7guaewm9np9uyaneitygk8', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rut, email })
        });
        const result = await response.json();

        // Enviar respuesta al cliente
        res.json({ message: `Resultado del proceso: ${result.someField}` });
    } else {
        res.status(405).send('Método no permitido');
    }
};

};
