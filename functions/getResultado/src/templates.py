from jinja2 import Environment, BaseLoader, select_autoescape

# Función para formatear números con separadores de miles
def format_currency(value):
    return f"{value:,.0f}".replace(',', '.')

# Función para formatear decimales con dos lugares
def format_decimal(value):
    return f"{value:.2f}"

# Crear un entorno de Jinja2 y agregar filtros
env = Environment(
    loader=BaseLoader(),
    autoescape=select_autoescape()
)
env.filters['currency'] = format_currency
env.filters['decimal'] = format_decimal

html_template = env.from_string("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Detalle del Documento</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Detalle del Documento</h1>
    <h2>Información Básica</h2>
    <ul>
        <li>RUT: {{ basic_info['rut'] }}</li>
        <li>Email: {{ basic_info['email'] }}</li>
        <li>Monto: {{ basic_info['monto']|currency }}</li>
        <li>Plazo: {{ basic_info['plazo'] }}</li>
        <li>Lista Negra: {{ basic_info['Lista Negra'] }}</li>
        <li>Lista Blanca: {{ basic_info['Lista Blanca'] }}</li>
        <li>Estado Crédito: {{ basic_info['estado_credito'] }}</li>
        <li>Total Deudas: {{ basic_info['total_deudas']|currency }}</li>
        <li>Score Crédito: {{ basic_info['score_credito'] }}</li>
    </ul>
    <h2>Resultado del Pricing</h2>
    <table>
        <thead>
            <tr>
                <th>SCORING DESDE (>=)</th>
                <th>SCORING HASTA (<)</th>
                <th>MONTO DESDE (>=)</th>
                <th>MONTO HASTA (<)</th>
                <th>PLAZO DESDE (DIAS >=)</th>
                <th>PLAZO HASTA (DIAS <)</th>
                <th>SPREAD (SOBRE TASA BASE)</th>
                <th>% DE ADELANTO</th>
                <th>MONEDA</th>
                <th>CANAL</th>
                <th>SEGMENTO</th>
                <th>ACCION</th>
            </tr>
        </thead>
        <tbody>
            {% for item in pricing_results %}
            <tr>
                <td>{{ item['SCORING DESDE (>=)'] }}</td>
                <td>{{ item['SCORING HASTA (<)'] }}</td>
                <td>{{ item['MONTO DESDE (>=)']|currency }}</td>
                <td>{{ item['MONTO HASTA (<)']|currency }}</td>
                <td>{{ item['PLAZO DESDE (DIAS >=)'] }}</td>
                <td>{{ item['PLAZO HASTA (DIAS <)'] }}</td>
                <td>{{ item['SPREAD (SOBRE TASA BASE)']|decimal }}</td>
                <td>{{ item['% DE ADELANTO'] }}</td>
                <td>{{ item['MONEDA'] }}</td>
                <td>{{ item['CANAL'] }}</td>
                <td>{{ item['SEGMENTO'] }}</td>
                <td>{{ item['ACCION'] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
""")

