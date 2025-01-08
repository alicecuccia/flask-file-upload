from flask import Flask, render_template, request
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import json

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

# Autenticazione con Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Carica le credenziali dalla variabile d'ambiente
credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if not credentials_json:
    raise EnvironmentError("La variabile d'ambiente GOOGLE_APPLICATION_CREDENTIALS non è impostata!")

try:
    creds = Credentials.from_service_account_info(json.loads(credentials_json), scopes=SCOPES)
except json.JSONDecodeError as e:
    raise EnvironmentError(f"Errore nel parsing del JSON delle credenziali: {e}")

# Inizializza il servizio Google Drive
drive_service = build('drive', 'v3', credentials=creds)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        files = request.files.getlist('file')

        if not name or not category or not files:
            return "Tutti i campi sono obbligatori!", 400

        try:
            # Crea una cartella per lo studente su Google Drive
            folder_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            student_folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
            student_folder_id = student_folder.get('id')
            print(f"Cartella dello studente creata con ID: {student_folder_id}")

            # Crea una sottocartella per la categoria
            subfolder_metadata = {
                'name': category,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [student_folder_id]
            }
            category_folder = drive_service.files().create(body=subfolder_metadata, fields='id').execute()
            category_folder_id = category_folder.get('id')
            print(f"Sottocartella della categoria creata con ID: {category_folder_id}")

            # Carica i file nella sottocartella
            for file in files:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))  # Salva temporaneamente
                file_metadata = {
                    'name': file.filename,
                    'parents': [category_folder_id]
                }
                media = MediaFileUpload(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                print(f"File caricato con ID: {uploaded_file.get('id')}")
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))  # Rimuovi dopo l'upload

            return "File caricati su Google Drive con successo!"
        except Exception as e:
            print(f"Errore durante il caricamento su Google Drive: {e}")
            return "Errore durante il caricamento su Google Drive.", 500

    return render_template('index.html', names=student_names, categories=site_elements)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
