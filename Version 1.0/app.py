from flask import Flask, render_template, request, send_file
import pandas as pd
import re
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    enunciado = request.form['enunciado']
    casos = generar_casos_detallados_simulado(enunciado)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet('Casos de Uso Detallados')

        header_format = workbook.add_format({
            'bold': True,
            'valign': 'top',
            'fg_color': '#4F81BD',
            'color': 'white',
            'border': 1
        })

        cell_format = workbook.add_format({
            'valign': 'top',
            'text_wrap': True,
            'border': 1
        })

        row = 0
        for caso in casos:
            for campo, valor in caso.items():
                worksheet.write(row, 0, campo, header_format)
                worksheet.write(row, 1, valor, cell_format)
                row += 1
            row += 1

        worksheet.set_column(0, 0, 30)
        worksheet.set_column(1, 1, 100)

    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name='casos_de_uso_detallados.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

def generar_casos_detallados_simulado(enunciado):
    accion, objeto = detectar_accion_objeto(enunciado)
    actor = inferir_actor(accion, objeto)
    flujo = generar_flujo_personalizado(accion, objeto)

    caso = {
        'Caso de uso': f'{accion.capitalize()} {objeto}',
        'Requerimientos relacionados': 'Req-01',
        'Objetivo en contexto': enunciado,
        'Precondiciones': 'El sistema está disponible y el actor tiene permisos.',
        'Final exitoso': f'{accion.capitalize()} realizado con éxito.',
        'Final fallido': f'La operación de {accion} es rechazada por error o permisos insuficientes.',
        'Actores principales': actor,
        'Actores secundarios': 'Sistema, servicios relacionados',
        'Evento de inicio': f'{actor} solicita {accion} {objeto}',
        'Flujo principal': flujo
    }
    return [caso]

def detectar_accion_objeto(texto):
    texto = texto.lower()
    equivalencias = {
        'revisión': 'verificar',
        'chequeo': 'verificar',
        'inspección': 'verificar',
        'creación': 'crear',
        'modificación': 'modificar',
        'eliminación': 'eliminar',
        'consulta': 'consultar',
        'registro': 'registrar',
        'autenticación': 'iniciar sesión',
        'login': 'iniciar sesión'
    }
    accion = 'realizar'
    objeto = 'operación'
    for clave, valor in equivalencias.items():
        if clave in texto:
            accion = valor
            break
    match = re.search(r'de (.+)', texto)
    if match:
        objeto = match.group(1)
    return accion, objeto.strip()

def inferir_actor(accion, objeto):
    if 'base de datos' in objeto or 'crud' in objeto:
        return 'DBA'
    if 'usuario' in objeto:
        return 'Administrador'
    if 'login' in objeto or 'sesión' in objeto:
        return 'Usuario final'
    return 'Usuario'

def generar_flujo_personalizado(accion, objeto):
    pasos = [
        f"1 - El actor identifica la necesidad de {accion} {objeto}.",
        f"2 - Accede al sistema correspondiente para iniciar el proceso.",
        f"3 - El sistema solicita la información necesaria para {accion} {objeto}.",
        f"4 - El actor proporciona la información requerida.",
        f"5 - El sistema valida los datos ingresados y las condiciones necesarias.",
        f"6 - El sistema ejecuta el proceso de {accion} {objeto}.",
        f"7 - El sistema almacena los resultados y actualiza el estado correspondiente.",
        f"8 - El sistema notifica al actor sobre la finalización del proceso."
    ]
    return '\n'.join(pasos)

if __name__ == '__main__':
    app.run(debug=True)
