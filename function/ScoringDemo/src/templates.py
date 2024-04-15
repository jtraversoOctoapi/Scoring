html_template = '''
<!doctype html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DEMO SCORING</title>
    <link rel="stylesheet" href="https://unpkg.com/pico.css">
    <script>
        function closeModal() {
            document.getElementById('modal').style.display = 'none';
         }
         
        document.addEventListener('DOMContentLoaded', function () {
            function openModal(response) {
                document.getElementById('responseText').value = response;
                document.getElementById('modal').style.display = 'flex';
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
                        if (response.ok) {
                            return response.json();
                        } else {
                            return response.text().then(text => Promise.reject('Error en la respuesta: ' + text));
                        }
                    })
                    .then(data => {
                        if (data.document_id) {
                            console.log('Datos recibidos:', data);
                            checkForResponse(data.document_id);  // Usamos document_id de la respuesta
                        } else {
                            console.error('Document_id no está presente en la respuesta');
                            document.getElementById('loader').style.display = 'none'; // Ocultar el loader si hay un error
                            alert('Ha ocurrido un error: ' + error); // Mostrar error al usuario
                        }
                    })
                    .catch(error => {
                        console.error('Error al enviar formulario:', error);
                    });
            });

        function checkForResponse(documentId) {
            console.log('Verificando respuesta para el documento', documentId, ' url:','https://661c32a7cbb49de418a6.appwrite.global/documents/${documentId)');
            const interval = setInterval(() => {
                fetch(`/documents/${documentId}`, {
                method: 'GET'
                })
                .then(response => {
                    console.log("response: ", response)
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    } else {
                        return response.json();
                    }
                })
                .then(data => {
                    console.log('Verificación de datos', data);
                    if (data.respuesta !== null) {
                        clearInterval(interval);
                        document.getElementById('loader').style.display = 'none';
                        openModal(data.respuesta);
                    }
                })
                .catch(error => {
                    console.error('Error al consultar el documento:', error.message);
                });
            }, 2000);
           }
        }); 
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
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 0 35px 0 35px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            background: #fff;
            border-radius: 8px;
            height: 25rem;
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
            width: calc(100%);
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
            line-height:1.25rem;
        }

        button {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
            height: 3rem;
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
            padding: 30px;
            left: 50%;
            top: calc(50% - 75px);
            transform: translate(-50%, -50%);
            z-index: 1000;
            background-color: rgba(0, 0, 0, 0.5);
            height:150px;
        }

        .spinner {
            border: 6px solid #f3f3f3;
            border-top: 6px solid #3498db;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 2s linear infinite;
            left: calc(50% - 25px);
            top: calc(50% - 75px);
            transform: translate(-50%, -50%);
            position: absolute;
        }

        .loading-text {
            color: white;
            top: 75px;
            position: relative;
            font-size: 22px;
            font-weight: 600;
        }

        /* Animación de giro */
        @keyframes spin {
            0% {
                transform: rotate(0deg);
            }

            100% {
                transform: rotate(360deg);
            }
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
        <div class="spinner"></div>
        <p class="loading-text">Esperando el resultado de tu evaluación...</p>
    </div>
    <div class="container">
        <h1>DEMO SCORING</h1>
        <form method="POST">
            <div>
                <label for="rut">RUT del Cliente:</label>
                <input type="text" id="rut" name="rut" required>
            </div>
            <div>
                <label for="email">Email de Notificación Resultado:</label>
                <input type="email" id="email" name="email" required>
            </div>
            <button type="submit">Enviar</button>
        </form>
    </div>
</body>

</html>
'''
