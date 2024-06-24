from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from app.api.routers import ocr
from fastapi.templating import Jinja2Templates

app = FastAPI()


app.include_router(ocr.app)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración de Jinja2 para los templates
templates = Jinja2Templates(directory="static/templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})