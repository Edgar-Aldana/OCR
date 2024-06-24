import cv2
import numpy as np
import requests
from googletrans import Translator
import base64
import pytesseract
from pytesseract import Output

# Configurar la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows



class OCRServices():

   
    def read_image(file) -> np.ndarray:
        image = np.fromstring(file, np.uint8)
        return cv2.imdecode(image, cv2.IMREAD_COLOR)

    def read_image_base64(data: str) -> np.ndarray:
        encoded_data = data.split(',')[1]
        decoded_data = base64.b64decode(encoded_data)
        np_data = np.frombuffer(decoded_data, np.uint8)
        return cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    def preprocess_image(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
        gray = cv2.medianBlur(gray, 3)  # Aplicar desenfoque para eliminar ruido
        return gray

    def extract_text(image):
        custom_config = r'--oem 3 --psm 6'  # Configuración para pytesseract
        details = pytesseract.image_to_data(image, output_type=Output.DICT, config=custom_config)
        text = " ".join([word for word in details['text'] if word.strip() != ''])  # Unir palabras no vacías
        return text

    
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

 
    def translate_text(text):
        translator = Translator()
        translated = translator.translate(text, src='en', dest='es')
        return translated.text

