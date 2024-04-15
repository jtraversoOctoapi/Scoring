import random

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
            # El RUT se podría extraer de la URL o de los parámetros de consulta
            rut = context.req.param('rut')
            if not rut:
                return context.res.json({'message': 'RUT is required'}, 400)
            
            # Genera datos aleatorios basados en el RUT proporcionado
            data = generate_random_data(rut)
            return context.res.json(data, 200)
        except Exception as e:
            return context.res.json({'error': str(e)}, 500)
    else:
        context.res.empty()
