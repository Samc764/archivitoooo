from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os

app = FastAPI()

DIRECTORIO_APP = os.path.dirname(os.path.abspath(__file__))
CARPETA_SUBIDAS = os.path.join("/tmp" if os.getenv("VERCEL") else DIRECTORIO_APP, "subidas")
os.makedirs(CARPETA_SUBIDAS, exist_ok=True)

app.mount("/archivos_cargados", StaticFiles(directory=CARPETA_SUBIDAS), name="archivos_cargados")
plantillas = Jinja2Templates(directory=os.path.join(DIRECTORIO_APP, "templates"))

@app.get("/", response_class=HTMLResponse)
async def inicio(peticion: Request):
    lista_archivos = os.listdir(CARPETA_SUBIDAS)
    return plantillas.TemplateResponse(
        request=peticion,
        name="index.html",
        context={"archivos": lista_archivos}
    )

@app.post("/upload")
async def cargar_archivo(fichero: UploadFile = File(...)):
    ruta_destino = os.path.join(CARPETA_SUBIDAS, fichero.filename)
    with open(ruta_destino, "wb") as buffer:
        shutil.copyfileobj(fichero.file, buffer)
    
    lista_actualizada = os.listdir(CARPETA_SUBIDAS)
    return {"mensaje": "Archivo subido exitosamente", "archivos": lista_actualizada}
