from flask import Flask, render_template, request, send_file
from generator import generar_tdcu_y_uxf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    enunciado = request.form['enunciado']
    excel_file, uxf_file = generar_tdcu_y_uxf(enunciado)

    # Devuelve un HTML sencillo mostrando los links
    return f"""
    <h1>Archivos generados</h1>
    <p><a href="/descargar/{excel_file}">Descargar TDCU (Excel)</a></p>
    <p><a href="/descargar/{uxf_file}">Descargar Diagrama (UXF)</a></p>
    <p><a href="/">Volver</a></p>
    """

@app.route('/descargar/<path:filename>')
def descargar(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)