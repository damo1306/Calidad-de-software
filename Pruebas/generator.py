import nltk

# Descarga punkt solo si no está disponible
nltk.download('punkt')  # Esto descarga el correcto

tokens = nltk.word_tokenize(enunciado)

from openpyxl import Workbook

# Asegúrate de descargar estos recursos de NLTK (hazlo una vez al inicio de tu app o en un script de instalación)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def analizar_enunciado(enunciado):
    tokens = nltk.word_tokenize(enunciado)
    tagged = nltk.pos_tag(tokens)

    print(f"Análisis gramatical: {tagged}")  # Esto es solo para debug

    # Intentamos encontrar verbos y sustantivos para enriquecer el análisis
    verbos = [word for word, pos in tagged if pos.startswith('VB')]
    sustantivos = [word for word, pos in tagged if pos.startswith('NN')]

    caso_uso = enunciado.strip().capitalize()

    actores = ['Usuario']  # Podríamos hacer que actores dependan del sustantivo
    acciones = []

    if verbos:
        acciones.append(f"Iniciar {verbos[0]} {sustantivos[0] if sustantivos else ''}".strip())
        acciones.append(f"Confirmar {verbos[0]} {sustantivos[0] if sustantivos else ''}".strip())
    else:
        acciones.append(f"Iniciar {caso_uso}")
        acciones.append(f"Confirmar {caso_uso}")

    return {
        'caso_uso': caso_uso,
        'actores': actores,
        'acciones': acciones
    }

def generar_tdcu_y_uxf(enunciado):
    datos = analizar_enunciado(enunciado)

    # Genera Excel
    excel_file = 'tdcu.xlsx'
    wb = Workbook()
    ws = wb.active
    ws.append(['Caso de uso', 'Actor', 'Acción'])
    for accion in datos['acciones']:
        ws.append([datos['caso_uso'], ', '.join(datos['actores']), accion])
    wb.save(excel_file)

    # Genera UXF
    uxf_file = 'diagrama_caso_uso.uxf'
    with open(uxf_file, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<diagram program="umlet" version="14.3.0">\n')

        for actor in datos['actores']:
            f.write(f'<element>\nActor\n{actor}\n</element>\n')

        f.write(f'<element>\nUseCase\n{datos["caso_uso"]}\n</element>\n')

        for actor in datos['actores']:
            f.write(f'<element>\nRelation\n{actor} -> {datos["caso_uso"]}\n</element>\n')

        f.write('</diagram>\n')

    return excel_file, uxf_file