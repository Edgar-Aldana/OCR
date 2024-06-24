from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse


from ..services.ocr_services import OCRServices


app = APIRouter()

@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    image = OCRServices.read_image(await file.read())
    preprocessed_image = OCRServices.preprocess_image(image)
    extracted_text = OCRServices.extract_text(preprocessed_image)
    corrected_text = OCRServices.spell_check(extracted_text)
    translated_text = OCRServices.translate_text(corrected_text)
    return JSONResponse(content={"extracted_text": corrected_text, "translated_text": translated_text})

@app.post("/process_camera/")
async def process_camera(data: dict):
    image = OCRServices.read_image_base64(data['image'])
    preprocessed_image = OCRServices.preprocess_image(image)
    extracted_text = OCRServices.extract_text(preprocessed_image)
    corrected_text = OCRServices.spell_check(extracted_text)
    translated_text = OCRServices.translate_text(corrected_text)
    return JSONResponse(content={"extracted_text": corrected_text, "translated_text": translated_text})


