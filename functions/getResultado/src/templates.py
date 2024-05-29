from jinja2 import Environment, Template

# Función para formatear números con separadores de miles
def format_currency(value):
    return "{:,.0f}".format(value).replace(",", ".")

# Función para redondear a dos decimales
def format_percentage(value):
    return "{:.2f}".format(value)

# Crear un entorno Jinja2 y añadir los filtros
env = Environment()
env.filters['currency'] = format_currency
env.filters['percentage'] = format_percentage

# Crear la plantilla con el entorno que tiene los filtros
html_template = env.from_string("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Detalle del Documento</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/picocss@1.0.0-beta.6/pico.min.css">
    <style>
        .responsive-table {
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <main class="container">
        <h1>Detalle del Documento</h1>
        <section>
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
        </section>
        <section>
            <h2>Resultado del Pricing</h2>
            <div class="responsive-table">
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
                            <td>{{ item['SPREAD (SOBRE TASA BASE)']|percentage }}</td>
                            <td>{{ item['% DE ADELANTO'] }}</td>
                            <td>{{ item['MONEDA'] }}</td>
                            <td>{{ item['CANAL'] }}</td>
                            <td>{{ item['SEGMENTO'] }}</td>
                            <td>{{ item['ACCION'] }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </section>
    </main>
</body>
</html>
""")

