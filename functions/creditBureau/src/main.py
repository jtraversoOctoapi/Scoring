import random
from appwrite.client import Client

# Initialize the Appwrite client
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1') \
      .set_project('661bf232a2d367eccb49') \
      .set_key('320f65e950d95bd0691e1373d8284014d835d8ba310b53180b96685f5df287cddc337e99f770952431dd1186beed8476940b19b001342ba7641a0d4a67d9297a7cfbfd0963579b44828298a308b651e06fc9a4224ab312a957e299233742e8e92e3511d5721926d9636b01afaccdecfeb805dde4af9ba838b6474bf76236a8de')

# Estados posibles para el crédito
credit_statuses = ["Normal", "Atrasado", "Moroso", "Sin Deudas"]

def generate_random_data(rut):
    """Genera datos ficticios basados en el RUT."""
    estado_credito = random.choice(credit_statuses)
    total_deudas = random.randint(0, 10000000)  # Total de deudas en CLP
    score_credito = random.randint(0, 1000)  # Score entre 0 y 1000

    return {
        "nombre": "Cliente " + rut,
        "rut": rut,
        "estado_credito": estado_credito,
        "total_deudas": total_deudas,
        "score_credito": score_credito
    }

def main(context):
    if context.req.method == 'GET':
        try:
            path_parts = context['request']['path'].split('/')
            if len(path_parts) >= 3 and path_parts[1] == 'rut':
                rut = path_parts[2]
                if rut:
                    data = generate_random_data(rut)
                    return context.res.json(data, 200)
                else:
                    return context.res.json({'message': 'RUT is required'}, 400)
            else:
                return context.res.json(({'message': 'Invalid path or missing RUT'}, 400)
        except Exception as e:
            return context.res.json({'error': str(e)}, 500)
    else:
        context['response'].empty()
