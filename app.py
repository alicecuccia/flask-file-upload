from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Configurazione della cartella di upload
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Lista di nomi degli studenti e categorie degli elementi
student_names = [
    "BANABESSE SEIDA", "BANCE FATIMATA", "BARA FATIMATA", "BELLO ARIANNA",
    "BENAHMED SABRINE", "BERNARDO MADDALENA", "BRAMBILLA KARYME LUCIA",
    "DIA DIOBA", "DIOP NDEYE ANTA", "ENNOUARI TASNIME", "FERRARI ASIA",
    "GASHI ELISA", "INVERNIZZI NADIA", "LEYE OMAR", "LIMEME IYED",
    "MARKU MARTINA", "MEDJMEDJ OUIJDAN", "MONTI ALESSIO", "NUZZO MARYLIN",
    "ORTEGA RALPH BRANDON", "PARWAZ RONAK BATUL", "PATUZZI AMY",
    "SCARPINO MATTIA", "VISMARA ILARIA", "ZOUMBARE BARKISSA"
]
site_elements = [
    "Hero Image", "Palette Colori", "Font o Tipografia", "Layout",
    "Pulsanti (CTA)", "Immagini e Icone", "Form", "Sezione Prezzi",
    "Sezione Testimonianze", "Sezione Contatti", "Sezione FAQ"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Dati dal form
        name = request.form['name']
        category = request.form['category']
        files = request.files.getlist('file')  # Ottieni tutti i file caricati

        # Verifica se tutti i campi sono compilati
        if not name or not category or not files:
            return "Tutti i campi sono obbligatori!", 400

        # Salva ogni file nella cartella corretta
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], name, category)
        os.makedirs(save_path, exist_ok=True)
        for file in files:
            file.save(os.path.join(save_path, file.filename))

        return "File caricati con successo!"

    return render_template('index.html', names=student_names, categories=site_elements)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

