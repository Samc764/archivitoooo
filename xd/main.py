from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os

app = FastAPI()

CARPETA_SUBIDAS = "/tmp/subidas" if os.getenv("VERCEL") else "subidas"
os.makedirs(CARPETA_SUBIDAS, exist_ok=True)

app.mount("/archivos_cargados", StaticFiles(directory=CARPETA_SUBIDAS), name="archivos_cargados")
plantillas = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def inicio(peticion: Request):
    lista_archivos = os.listdir(CARPETA_SUBIDAS)
    return plantillas.TemplateResponse("index.html", {
        "request": peticion,
        "archivos": lista_archivos
    })

@app.post("/upload")
async def cargar_archivo(fichero: UploadFile = File(...)):
    ruta_destino = os.path.join(CARPETA_SUBIDAS, fichero.filename)
    with open(ruta_destino, "wb") as buffer:
        shutil.copyfileobj(fichero.file, buffer)
    
    lista_actualizada = os.listdir(CARPETA_SUBIDAS)
    return {"mensaje": "Archivo subido exitosamente", "archivos": lista_actualizada}
