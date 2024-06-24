import cv2
import pytesseract
from pytesseract import Output
import requests
from googletrans import Translator


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 1. Adquisición de la imagen
def load_image(image_path):
    return cv2.imread(image_path)

# 2. Preprocesamiento de la imagen
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
    gray = cv2.medianBlur(gray, 3)  # Aplicar desenfoque para eliminar ruido
    return gray

# 3. OCR para extraer texto de la imagen
def extract_text(image):
    custom_config = r'--oem 3 --psm 6'  # Configuración para pytesseract
    details = pytesseract.image_to_data(image, output_type=Output.DICT, config=custom_config)
    text = " ".join(details['text'])
    return text

# 4. Verificación y corrección ortográfica
def spell_check(text):
    words = text.split()
    corrected_words = []
    for word in words:
        response = requests.get(f"https://api.datamuse.com/words?sp={word}&max=1")
        if response.status_code == 200 and len(response.json()) > 0:
            corrected_words.append(response.json()[0]['word'])
        else:
            corrected_words.append(word)
    return " ".join(corrected_words)

# 5. Traducción del texto
def translate_text(text):
    translator = Translator()
    translated = translator.translate(text, src='en', dest='es')
    return translated.text

# Función principal del sistema
def main(image_path):
    # Cargar y preprocesar la imagen
    image = load_image(image_path)
    preprocessed_image = preprocess_image(image)
    
    # Extraer texto utilizando OCR
    extracted_text = extract_text(preprocessed_image)
    
    # Verificar y corregir el texto extraído
    corrected_text = spell_check(extracted_text)
    
    # Traducir el texto corregido
    translated_text = translate_text(corrected_text)
    
    # Mostrar el texto traducido
    print("Texto traducido:")
    print(translated_text)


# Prueba del sistema con una imagen de entrada
image_path = 'test.jpg'  # Especificar la ruta a la imagen
main(image_path)



