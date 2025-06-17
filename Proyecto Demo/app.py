from flask import Flask, request, render_template, send_file
from generador_uxf import generar_uxf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    enunciado = request.form['enunciado']
    ruta_archivo = generar_uxf(enunciado)
    return send_file(ruta_archivo, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)