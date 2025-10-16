import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from loader import cargar_vectorstore
from dotenv import load_dotenv
from local_llm import responder_con_llm  # Ahora usa GPT

load_dotenv()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

modelos_disponibles = ["FT125", "FT150"]
vectorstores = {modelo: cargar_vectorstore(modelo) for modelo in modelos_disponibles}

class Pregunta(BaseModel):
    modelo: str
    pregunta: str

@app.post("/preguntar")
def responder(data: Pregunta):
    modelo = data.modelo.upper()
    if modelo not in vectorstores:
        raise HTTPException(status_code=404, detail="Modelo no encontrado.")
    
    docs = vectorstores[modelo].similarity_search(data.pregunta, k=3)
    contexto = "\n".join([doc.page_content for doc in docs])
    respuesta = responder_con_llm(data.pregunta, contexto)

    return {"respuesta": respuesta}
